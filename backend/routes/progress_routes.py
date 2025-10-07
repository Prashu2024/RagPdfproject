from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from config.database import get_db
from services.analytics_service import analytics_service
from schemas.pdf_schema import UserProgress

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user progress and analytics
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Dictionary with user progress analytics
    """
    try:
        # Calculate user progress
        progress = analytics_service.calculate_user_progress(db, user_id)
        
        return {
            "success": True,
            "data": progress
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/insights")
async def get_learning_insights(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get learning insights for the user
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Dictionary with learning insights
    """
    try:
        # Get learning insights
        insights = analytics_service.get_learning_insights(db, user_id)
        
        return {
            "success": True,
            "data": insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/study-patterns")
async def get_study_patterns(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user study patterns
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Dictionary with study patterns
    """
    try:
        # Get study patterns
        patterns = analytics_service._analyze_study_patterns(db, user_id)
        
        return {
            "success": True,
            "data": patterns
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/goals")
async def get_learning_goals(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get suggested learning goals for the user
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Dictionary with suggested learning goals
    """
    try:
        # Get user progress first
        progress = analytics_service.calculate_user_progress(db, user_id)
        
        # Get suggested goals
        goals = analytics_service._suggest_goals(progress)
        
        return {
            "success": True,
            "data": {
                "goals": goals,
                "current_progress": progress
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=50, description="Number of top users to return"),
    db: Session = Depends(get_db)
):
    """
    Get leaderboard of top users
    
    Args:
        limit: Number of top users to return
        db: Database session
        
    Returns:
        List of top users with their scores
    """
    try:
        from models.pdf_model import QuizAttempt, User
        
        # Get top users by average score
        top_users = db.query(
            User.id,
            User.username,
            func.avg(QuizAttempt.score).label('average_score'),
            func.count(QuizAttempt.id).label('total_quizzes')
        ).join(
            QuizAttempt, User.id == QuizAttempt.user_id
        ).filter(
            QuizAttempt.score.isnot(None)
        ).group_by(
            User.id, User.username
        ).order_by(
            func.avg(QuizAttempt.score).desc()
        ).limit(limit).all()
        
        leaderboard = []
        for user in top_users:
            leaderboard.append({
                "user_id": user.id,
                "username": user.username,
                "average_score": round(user.average_score or 0, 2),
                "total_quizzes": user.total_quizzes,
                "rank": leaderboard.index(user) + 1
            })
        
        return {
            "success": True,
            "data": {
                "leaderboard": leaderboard,
                "total_users": db.query(User).count()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/overview")
async def get_overall_stats(db: Session = Depends(get_db)):
    """
    Get overall platform statistics
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with overall platform statistics
    """
    try:
        from models.pdf_model import User, QuizAttempt, PDF
        from datetime import datetime, timedelta
        
        # Get basic counts
        total_users = db.query(User).count()
        total_pdfs = db.query(PDF).count()
        total_quiz_attempts = db.query(QuizAttempt).count()
        
        # Get average quiz score
        avg_score = db.query(func.avg(QuizAttempt.score)).filter(
            QuizAttempt.score.isnot(None)
        ).scalar() or 0
        
        # Get recent activity (last 7 days) - SQLite compatible
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_attempts = db.query(QuizAttempt).filter(
            QuizAttempt.completed_at >= seven_days_ago
        ).count()
        
        return {
            "success": True,
            "data": {
                "total_users": total_users,
                "total_pdfs": total_pdfs,
                "total_quiz_attempts": total_quiz_attempts,
                "average_quiz_score": round(avg_score, 2),
                "recent_activity": recent_attempts,
                "platform_uptime": "100%"  # In production, track actual uptime
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))