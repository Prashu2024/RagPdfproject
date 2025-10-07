import json
import openai
from typing import List, Dict, Optional
from config.llm_config import llm_config
from schemas.pdf_schema import QuizQuestion, QuizResponse

class QuizGenerator:
    """Service for generating quizzes using LLMs"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=llm_config.openai_api_key)
    
    def generate_quiz_from_content(self, content: str, quiz_type: str = "MCQ", num_questions: int = 5) -> QuizResponse:
        """
        Generate quiz from provided content
        
        Args:
            content: Text content to generate quiz from
            quiz_type: Type of quiz (MCQ, SAQ, LAQ)
            num_questions: Number of questions to generate
            
        Returns:
            QuizResponse object with generated questions
        """
        try:
            # Prepare prompt
            prompt = llm_config.quiz_generation_prompt.format(
                question_type=quiz_type,
                content=content,
                num_questions=num_questions
            )
            
            # Generate quiz using OpenAI
            response = self.openai_client.chat.completions.create(
                model=llm_config.openai_model,
                messages=[
                    {"role": "system", "content": "You are an educational quiz generator. Generate high-quality quiz questions based on the provided content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=llm_config.openai_temperature,
                max_tokens=llm_config.openai_max_tokens
            )
            
            # Parse response
            quiz_data = json.loads(response.choices[0].message.content)
            
            # Convert to QuizResponse
            questions = []
            for q_data in quiz_data.get('questions', []):
                question = QuizQuestion(
                    question=q_data.get('question', ''),
                    type=q_data.get('type', quiz_type),
                    difficulty=q_data.get('difficulty', 'Medium'),
                    options=q_data.get('options', []) if quiz_type == 'MCQ' else None,
                    correct_answer=q_data.get('correct_answer', ''),
                    explanation=q_data.get('explanation', '')
                )
                questions.append(question)
            
            return QuizResponse(questions=questions)
            
        except json.JSONDecodeError:
            # Fallback: create simple questions if JSON parsing fails
            return self._create_fallback_quiz(content, quiz_type, num_questions)
        except Exception as e:
            raise Exception(f"Error generating quiz: {str(e)}")
    
    def generate_quiz_from_pdf(self, pdf_id: int, db_session, quiz_type: str = "MCQ", num_questions: int = 5) -> QuizResponse:
        """
        Generate quiz from PDF content
        
        Args:
            pdf_id: ID of the PDF
            db_session: Database session
            quiz_type: Type of quiz (MCQ, SAQ, LAQ)
            num_questions: Number of questions to generate
            
        Returns:
            QuizResponse object with generated questions
        """
        try:
            # Get text chunks for the PDF
            from ..models.pdf_model import TextChunk
            
            chunks = db_session.query(TextChunk).filter(TextChunk.pdf_id == pdf_id).all()
            
            if not chunks:
                raise Exception("No text chunks found for the specified PDF")
            
            # Combine chunks for quiz generation
            combined_content = " ".join([chunk.chunk_text for chunk in chunks])
            
            # Limit content length for LLM
            if len(combined_content) > 8000:
                combined_content = combined_content[:8000] + "... [content truncated]"
            
            return self.generate_quiz_from_content(combined_content, quiz_type, num_questions)
            
        except Exception as e:
            raise Exception(f"Error generating quiz from PDF: {str(e)}")
    
    def evaluate_quiz_answers(self, questions: List[QuizQuestion], user_answers: List[str]) -> Dict:
        """
        Evaluate user answers against correct answers
        
        Args:
            questions: List of QuizQuestion objects
            user_answers: List of user answers
            
        Returns:
            Dictionary with evaluation results
        """
        if len(questions) != len(user_answers):
            raise Exception("Number of questions and answers must match")
        
        results = {
            'total_questions': len(questions),
            'correct_answers': 0,
            'incorrect_answers': 0,
            'score': 0,
            'answers': []
        }
        
        for i, (question, user_answer) in enumerate(zip(questions, user_answers)):
            is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
            
            if is_correct:
                results['correct_answers'] += 1
            else:
                results['incorrect_answers'] += 1
            
            results['answers'].append({
                'question_number': i + 1,
                'question': question.question,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation
            })
        
        # Calculate score
        results['score'] = int((results['correct_answers'] / results['total_questions']) * 100)
        
        return results
    
    def _create_fallback_quiz(self, content: str, quiz_type: str, num_questions: int) -> QuizResponse:
        """Create fallback quiz if LLM response parsing fails"""
        questions = []
        
        # Simple keyword-based questions for fallback
        sentences = content.split('.')[:num_questions]
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                question = QuizQuestion(
                    question=f"What is the main idea in this sentence: '{sentence.strip()}'?",
                    type=quiz_type,
                    difficulty="Easy",
                    options=None if quiz_type != "MCQ" else ["Option 1", "Option 2", "Option 3", "Option 4"],
                    correct_answer="The main idea is about the content discussed",
                    explanation="This is a fallback question based on the provided content."
                )
                questions.append(question)
        
        return QuizResponse(questions=questions)
    
    def get_quiz_statistics(self, quiz_results: Dict) -> Dict:
        """
        Generate statistics from quiz results
        
        Args:
            quiz_results: Dictionary with quiz evaluation results
            
        Returns:
            Dictionary with statistics and insights
        """
        stats = {
            'score_percentage': quiz_results['score'],
            'accuracy_rate': quiz_results['correct_answers'] / quiz_results['total_questions'],
            'difficulty_distribution': {'Easy': 0, 'Medium': 0, 'Hard': 0},
            'topic_performance': {},
            'improvement_suggestions': []
        }
        
        # Analyze answers for insights
        for answer in quiz_results['answers']:
            # This would be enhanced with actual topic analysis
            topic = "General"  # In real implementation, extract topic from question
            
            if topic not in stats['topic_performance']:
                stats['topic_performance'][topic] = {'correct': 0, 'total': 0}
            
            stats['topic_performance'][topic]['total'] += 1
            if answer['is_correct']:
                stats['topic_performance'][topic]['correct'] += 1
        
        # Generate improvement suggestions
        if stats['accuracy_rate'] < 0.5:
            stats['improvement_suggestions'].append("Focus on understanding the basic concepts")
        elif stats['accuracy_rate'] < 0.8:
            stats['improvement_suggestions'].append("Review the topics where you made mistakes")
        else:
            stats['improvement_suggestions'].append("Great job! Try more challenging questions")
        
        return stats

# Global quiz generator instance
quiz_generator = QuizGenerator()
