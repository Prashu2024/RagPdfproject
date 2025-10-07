
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import uuid
from datetime import datetime
from config.database import get_db
from models.pdf_model import PDF, QuizAttempt, User, TextChunk
from schemas.pdf_schema import (
    QuizResponse, QuizQuestion, QuizResult, QuizSubmission,
    QuizAnswer, QuizAttempt as QuizAttemptSchema
)
from utils.quiz_generator import quiz_generator
from services.analytics_service import analytics_service

router = APIRouter()

@router.post("/generate")
async def generate_quiz(
    pdf_id: int = None,
    quiz_type: str = "MCQ",
    num_questions: int = 5,
    db: Session = Depends(get_db)
):
    """
    Generates a quiz from the specified PDF or all PDFs if no PDF is specified.
    """
    try:
        # Validate quiz type
        valid_quiz_types = ["MCQ", "SAQ", "LAQ"]
        if quiz_type not in valid_quiz_types:
            raise HTTPException(status_code=400, detail=f"Invalid quiz type. Must be one of: {valid_quiz_types}")
        
        # Validate number of questions
        if num_questions < 1 or num_questions > 20:
            raise HTTPException(status_code=400, detail="Number of questions must be between 1 and 20")
        
        # Get current user (simplified)
        user_id = 1  # For demo purposes
        
        if pdf_id is not None:
            # Generate quiz from specific PDF
            pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
            if not pdf:
                raise HTTPException(status_code=404, detail="PDF not found")
            
            # Check if PDF is processed
            if not pdf.processed:
                raise HTTPException(status_code=400, detail="PDF is not processed yet. Please wait for processing to complete.")
            
            # Generate quiz from specific PDF
            quiz_response = quiz_generator.generate_quiz_from_pdf(pdf_id, db, quiz_type, num_questions)
        else:
            # Generate quiz from all processed PDFs
            processed_pdfs = db.query(PDF).filter(PDF.processed == True).all()
            if not processed_pdfs:
                raise HTTPException(status_code=400, detail="No processed PDFs available for quiz generation")
            
            # Generate quiz from all PDFs
            quiz_response = quiz_generator.generate_quiz_from_all_pdfs(db, quiz_type, num_questions)
        
        # Create quiz attempt record
        quiz_attempt = QuizAttempt(
            pdf_id=pdf_id,
            user_id=user_id,
            quiz_type=quiz_type,
            total_questions=num_questions,
            answers=json.dumps([{
                "question": q.question,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation
            } for q in quiz_response.questions])
        )
        
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)
        
        return {
            "success": True,
            "data": {
                "quiz_id": quiz_attempt.id,
                "pdf_id": pdf_id,
                "quiz_type": quiz_type,
                "total_questions": num_questions,
                "questions": quiz_response.questions,
                "created_at": quiz_attempt.completed_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_quiz_statistics(
    pdf_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get quiz statistics.
    """
    try:
        from sqlalchemy import func
        
        # Build query
        query = db.query(QuizAttempt)
        
        if pdf_id:
            query = query.filter(QuizAttempt.pdf_id == pdf_id)
        
        if user_id:
            query = query.filter(QuizAttempt.user_id == user_id)
        
        # Get statistics
        total_attempts = query.count()
        average_score = db.query(func.avg(QuizAttempt.score)).filter(
            QuizAttempt.score.isnot(None)
        ).scalar() or 0
        
        # Get score distribution
        from sqlalchemy import case
        
        score_case = case(
            (QuizAttempt.score >= 80, 'Excellent'),
            (QuizAttempt.score >= 60, 'Good'),
            (QuizAttempt.score >= 40, 'Average'),
            else_='Poor'
        )
        
        score_distribution = db.query(
            score_case.label('category'),
            func.count(QuizAttempt.id).label('count')
        ).filter(
            QuizAttempt.score.isnot(None)
        ).group_by(score_case).all()
        
        # Get quiz type distribution
        quiz_type_distribution = db.query(
            QuizAttempt.quiz_type,
            func.count(QuizAttempt.id).label('count')
        ).filter(
            QuizAttempt.score.isnot(None)
        ).group_by(QuizAttempt.quiz_type).all()
        
        return {
            "success": True,
            "data": {
                "total_attempts": total_attempts,
                "average_score": round(average_score, 2),
                "score_distribution": [
                    {"category": category, "count": count}
                    for category, count in score_distribution
                ],
                "quiz_type_distribution": [
                    {"type": quiz_type, "count": count}
                    for quiz_type, count in quiz_type_distribution
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{quiz_id}")
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a specific quiz.
    """
    try:
        quiz_attempt = db.query(QuizAttempt).filter(QuizAttempt.id == quiz_id).first()
        
        if not quiz_attempt:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        # Parse questions from stored answers
        questions_data = json.loads(quiz_attempt.answers) if quiz_attempt.answers else []
        
        questions = []
        for q_data in questions_data:
            question = QuizQuestion(
                question=q_data.get('question', ''),
                type=quiz_attempt.quiz_type,
                difficulty="Medium",  # Default difficulty
                options=None,  # Would be stored in production
                correct_answer=q_data.get('correct_answer', ''),
                explanation=q_data.get('explanation', '')
            )
            questions.append(question)
        
        return {
            "success": True,
            "data": {
                "quiz_id": quiz_id,
                "pdf_id": quiz_attempt.pdf_id,
                "quiz_type": quiz_attempt.quiz_type,
                "total_questions": quiz_attempt.total_questions,
                "questions": questions,
                "created_at": quiz_attempt.completed_at,
                "completed": quiz_attempt.score is not None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db: Session = Depends(get_db)
):
    """
    Submit quiz answers and get results.
    """
    try:
        # Get quiz attempt
        quiz_attempt = db.query(QuizAttempt).filter(QuizAttempt.id == quiz_id).first()
        
        if not quiz_attempt:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        if quiz_attempt.score is not None:
            raise HTTPException(status_code=400, detail="Quiz already submitted")
        
        # Get quiz questions
        questions_data = json.loads(quiz_attempt.answers) if quiz_attempt.answers else []
        
        # Create QuizQuestion objects
        questions = []
        for q_data in questions_data:
            question = QuizQuestion(
                question=q_data.get('question', ''),
                type=quiz_attempt.quiz_type,
                difficulty="Medium",
                options=None,
                correct_answer=q_data.get('correct_answer', ''),
                explanation=q_data.get('explanation', '')
            )
            questions.append(question)
        
        # Extract user answers
        user_answers = [answer.answer for answer in submission.answers]
        
        # Evaluate quiz
        evaluation_result = quiz_generator.evaluate_quiz_answers(questions, user_answers)
        
        # Update quiz attempt
        quiz_attempt.score = evaluation_result['score']
        # Convert QuizAnswer objects to dictionaries for JSON serialization
        answers_dict = [answer.dict() for answer in submission.answers]
        quiz_attempt.answers = json.dumps(answers_dict)
        db.commit()
        
        # Update user progress
        analytics_service.update_user_progress(db, quiz_attempt.user_id, evaluation_result)
        
        return {
            "success": True,
            "data": {
                "quiz_id": quiz_id,
                "score": evaluation_result['score'],
                "total_questions": evaluation_result['total_questions'],
                "correct_answers": evaluation_result['correct_answers'],
                "incorrect_answers": evaluation_result['incorrect_answers'],
                "answers": evaluation_result['answers'],
                "completed_at": datetime.now()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/attempts")
async def get_user_quiz_attempts(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get quiz attempts for a specific user.
    """
    try:
        # Get quiz attempts
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user_id
        ).order_by(QuizAttempt.completed_at.desc()).offset(offset).limit(limit).all()
        
        # Convert to schema format
        attempt_schemas = []
        for attempt in attempts:
            attempt_schemas.append({
                "id": attempt.id,
                "pdf_id": attempt.pdf_id,
                "quiz_type": attempt.quiz_type,
                "score": attempt.score,
                "total_questions": attempt.total_questions,
                "completed_at": attempt.completed_at,
                "answers": json.loads(attempt.answers) if attempt.answers else []
            })
        
        return {
            "success": True,
            "data": {
                "attempts": attempt_schemas,
                "total_count": len(attempts),
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pdf/{pdf_id}/attempts")
async def get_pdf_quiz_attempts(
    pdf_id: int,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get quiz attempts for a specific PDF.
    """
    try:
        # Validate PDF exists
        pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Get quiz attempts
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.pdf_id == pdf_id
        ).order_by(QuizAttempt.completed_at.desc()).offset(offset).limit(limit).all()
        
        # Convert to schema format
        attempt_schemas = []
        for attempt in attempts:
            attempt_schemas.append({
                "id": attempt.id,
                "user_id": attempt.user_id,
                "quiz_type": attempt.quiz_type,
                "score": attempt.score,
                "total_questions": attempt.total_questions,
                "completed_at": attempt.completed_at
            })
        
        return {
            "success": True,
            "data": {
                "attempts": attempt_schemas,
                "total_count": len(attempts),
                "limit": limit,
                "offset": offset
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
