from typing import Dict, List, Optional
from sqlalchemy import func
from models.pdf_model import QuizAttempt, UserProgress, TextChunk
from schemas.pdf_schema import UserProgressCreate
import json

class AnalyticsService:
    """Service for tracking user progress and analytics"""
    
    def calculate_user_progress(self, db_session, user_id: int) -> Dict:
        """
        Calculate user progress based on quiz attempts
        
        Args:
            db_session: Database session
            user_id: User ID to calculate progress for
            
        Returns:
            Dictionary with progress analytics
        """
        try:
            # Get all quiz attempts for the user
            attempts = db_session.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
            
            if not attempts:
                return {
                    'user_id': user_id,
                    'total_quizzes': 0,
                    'average_score': 0,
                    'progress_by_topic': {},
                    'strengths': [],
                    'weaknesses': [],
                    'improvement_trend': 'stable'
                }
            
            # Calculate overall statistics
            total_quizzes = len(attempts)
            average_score = sum(attempt.score for attempt in attempts if attempt.score) / total_quizzes
            
            # Progress by topic (PDF)
            progress_by_topic = {}
            for attempt in attempts:
                pdf_info = db_session.query(TextChunk).filter(TextChunk.pdf_id == attempt.pdf_id).first()
                topic = f"PDF {attempt.pdf_id}"  # In real implementation, extract topic from PDF
                
                if topic not in progress_by_topic:
                    progress_by_topic[topic] = {
                        'total_attempts': 0,
                        'average_score': 0,
                        'quiz_types': set()
                    }
                
                progress_by_topic[topic]['total_attempts'] += 1
                if attempt.score:
                    progress_by_topic[topic]['average_score'] += attempt.score
                progress_by_topic[topic]['quiz_types'].add(attempt.quiz_type)
            
            # Calculate average scores for each topic
            for topic, data in progress_by_topic.items():
                if data['total_attempts'] > 0:
                    data['average_score'] = data['average_score'] / data['total_attempts']
                data['quiz_types'] = list(data['quiz_types'])
            
            # Identify strengths and weaknesses
            strengths = []
            weaknesses = []
            
            for topic, data in progress_by_topic.items():
                if data['average_score'] >= 80:
                    strengths.append({
                        'topic': topic,
                        'score': data['average_score'],
                        'attempts': data['total_attempts']
                    })
                elif data['average_score'] < 60:
                    weaknesses.append({
                        'topic': topic,
                        'score': data['average_score'],
                        'attempts': data['total_attempts']
                    })
            
            # Sort by score
            strengths.sort(key=lambda x: x['score'], reverse=True)
            weaknesses.sort(key=lambda x: x['score'])
            
            # Calculate improvement trend
            improvement_trend = self._calculate_improvement_trend(attempts)
            
            return {
                'user_id': user_id,
                'total_quizzes': total_quizzes,
                'average_score': round(average_score, 2),
                'progress_by_topic': progress_by_topic,
                'strengths': strengths[:5],  # Top 5 strengths
                'weaknesses': weaknesses[:5],  # Top 5 weaknesses
                'improvement_trend': improvement_trend
            }
            
        except Exception as e:
            raise Exception(f"Error calculating user progress: {str(e)}")
    
    def update_user_progress(self, db_session, user_id: int, quiz_result: Dict) -> UserProgress:
        """
        Update user progress based on quiz result
        
        Args:
            db_session: Database session
            user_id: User ID
            quiz_result: Quiz result dictionary
            
        Returns:
            Updated UserProgress object
        """
        try:
            # Extract topic from quiz result (simplified)
            topic = "General"  # In real implementation, extract from PDF content
            
            # Get existing progress
            progress = db_session.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.topic == topic
            ).first()
            
            if progress:
                # Update existing progress
                total_attempts = progress.strength_score * 10 + 1  # Approximate
                new_strength_score = (progress.strength_score * (total_attempts - 1) + quiz_result['score']) / total_attempts
                
                progress.strength_score = min(new_strength_score, 1.0)
                progress.weakness_score = max(1.0 - new_strength_score, 0.0)
                progress.last_updated = func.now()
            else:
                # Create new progress entry
                progress = UserProgress(
                    user_id=user_id,
                    topic=topic,
                    strength_score=quiz_result['score'] / 100,
                    weakness_score=1.0 - (quiz_result['score'] / 100)
                )
                db_session.add(progress)
            
            db_session.commit()
            db_session.refresh(progress)
            
            return progress
            
        except Exception as e:
            db_session.rollback()
            raise Exception(f"Error updating user progress: {str(e)}")
    
    def get_learning_insights(self, db_session, user_id: int) -> Dict:
        """
        Generate learning insights for the user
        
        Args:
            db_session: Database session
            user_id: User ID
            
        Returns:
            Dictionary with learning insights
        """
        try:
            progress = self.calculate_user_progress(db_session, user_id)
            
            insights = {
                'overall_performance': self._categorize_performance(progress['average_score']),
                'recommendations': self._generate_recommendations(progress),
                'study_patterns': self._analyze_study_patterns(db_session, user_id),
                'goal_suggestions': self._suggest_goals(progress)
            }
            
            return insights
            
        except Exception as e:
            raise Exception(f"Error generating learning insights: {str(e)}")
    
    def _calculate_improvement_trend(self, attempts: List[QuizAttempt]) -> str:
        """Calculate improvement trend based on recent attempts"""
        if len(attempts) < 3:
            return 'insufficient_data'
        
        # Sort by completion date
        sorted_attempts = sorted(attempts, key=lambda x: x.completed_at, reverse=True)
        recent_attempts = sorted_attempts[:5]  # Last 5 attempts
        
        # Calculate trend
        scores = [attempt.score for attempt in recent_attempts if attempt.score]
        
        if len(scores) < 2:
            return 'insufficient_data'
        
        # Simple trend calculation
        if scores[-1] > scores[0] + 10:
            return 'improving'
        elif scores[-1] < scores[0] - 10:
            return 'declining'
        else:
            return 'stable'
    
    def _categorize_performance(self, average_score: float) -> str:
        """Categorize user performance"""
        if average_score >= 90:
            return 'excellent'
        elif average_score >= 80:
            return 'good'
        elif average_score >= 70:
            return 'average'
        elif average_score >= 60:
            return 'below_average'
        else:
            return 'needs_improvement'
    
    def _generate_recommendations(self, progress: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Based on overall performance
        if progress['average_score'] < 70:
            recommendations.append("Focus on understanding basic concepts before moving to advanced topics")
        
        # Based on strengths and weaknesses
        if progress['weaknesses']:
            weakest_topic = progress['weaknesses'][0]['topic']
            recommendations.append(f"Review {weakest_topic} as it appears to be a weakness area")
        
        # Based on improvement trend
        if progress['improvement_trend'] == 'declining':
            recommendations.append("Consider reviewing recent study materials and taking more practice quizzes")
        elif progress['improvement_trend'] == 'improving':
            recommendations.append("Great progress! Keep up the good momentum")
        
        # Based on quiz diversity
        quiz_types = set()
        for topic_data in progress['progress_by_topic'].values():
            quiz_types.update(topic_data['quiz_types'])
        
        if len(quiz_types) == 1:
            recommendations.append("Try different types of quizzes to enhance learning")
        
        return recommendations
    
    def _analyze_study_patterns(self, db_session, user_id: int) -> Dict:
        """Analyze user study patterns"""
        try:
            from sqlalchemy import extract
            
            # Get attempts by month
            monthly_attempts = db_session.query(
                extract('month', QuizAttempt.completed_at).label('month'),
                extract('year', QuizAttempt.completed_at).label('year'),
                func.count(QuizAttempt.id).label('count')
            ).filter(QuizAttempt.user_id == user_id).group_by(
                extract('year', QuizAttempt.completed_at),
                extract('month', QuizAttempt.completed_at)
            ).order_by(
                extract('year', QuizAttempt.completed_at),
                extract('month', QuizAttempt.completed_at)
            ).all()
            
            # Get preferred quiz types
            quiz_type_stats = db_session.query(
                QuizAttempt.quiz_type,
                func.count(QuizAttempt.id).label('count')
            ).filter(QuizAttempt.user_id == user_id).group_by(QuizAttempt.quiz_type).all()
            
            return {
                'monthly_activity': [
                    {'month': f"{year}-{month:02d}", 'count': count}
                    for year, month, count in monthly_attempts
                ],
                'preferred_quiz_types': [
                    {'type': quiz_type, 'count': count}
                    for quiz_type, count in quiz_type_stats
                ]
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _suggest_goals(self, progress: Dict) -> List[Dict]:
        """Suggest learning goals"""
        goals = []
        
        # Score-based goals
        if progress['average_score'] < 80:
            goals.append({
                'type': 'score_improvement',
                'target': 'Achieve 80% average score',
                'timeline': '2 weeks',
                'description': 'Focus on understanding core concepts and practice regularly'
            })
        
        # Topic-based goals
        if progress['weaknesses']:
            weakest_topic = progress['weaknesses'][0]['topic']
            goals.append({
                'type': 'topic_mastery',
                'target': f'Master {weakest_topic}',
                'timeline': '1 week',
                'description': f'Extra practice on {weakest_topic} with targeted quizzes'
            })
        
        # Diversity goals
        quiz_types = set()
        for topic_data in progress['progress_by_topic'].values():
            quiz_types.update(topic_data['quiz_types'])
        
        if len(quiz_types) < 3:
            goals.append({
                'type': 'quiz_diversity',
                'target': 'Try all quiz types',
                'timeline': '1 week',
                'description': 'Practice MCQ, SAQ, and LAQ questions for comprehensive learning'
            })
        
        return goals

# Global analytics service instance
analytics_service = AnalyticsService()