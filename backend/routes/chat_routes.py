from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db
from services.rag_service import rag_service
from utils.youtube_recommender import youtube_recommender

router = APIRouter()

@router.post("/ask")
async def ask_question(
    question: str,
    pdf_id: Optional[int] = Query(None, description="Optional PDF ID to search within"),
    db: Session = Depends(get_db)
):
    """
    Ask a question using RAG with PDF content
    
    Args:
        question: User question
        pdf_id: Optional PDF ID to search within
        db: Database session
        
    Returns:
        Dictionary with answer and citations
    """
    try:
        # Get answer using RAG
        result = rag_service.ask_question(question, pdf_id)
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
async def explain_concept(
    concept: str,
    pdf_id: Optional[int] = Query(None, description="Optional PDF ID to search within"),
    db: Session = Depends(get_db)
):
    """
    Explain a concept using the PDF content
    
    Args:
        concept: Concept to explain
        pdf_id: Optional PDF ID to search within
        db: Database session
        
    Returns:
        Dictionary with explanation and examples
    """
    try:
        # Get explanation using RAG
        result = rag_service.explain_concept(concept, pdf_id)
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar-topics")
async def get_similar_topics(
    query: str,
    pdf_id: Optional[int] = Query(None, description="Optional PDF ID to search within"),
    top_k: int = Query(5, ge=1, le=20, description="Number of results to return"),
    db: Session = Depends(get_db)
):
    """
    Find similar topics or content in the PDF
    
    Args:
        query: Search query
        pdf_id: Optional PDF ID to search within
        top_k: Number of results to return
        db: Database session
        
    Returns:
        List of similar content with metadata
    """
    try:
        # Get similar topics
        result = rag_service.get_similar_topics(query, pdf_id, top_k)
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend-videos")
async def recommend_videos(
    topic: str,
    content_summary: str = Query("", description="Content summary for context"),
    max_results: int = Query(5, ge=1, le=10, description="Maximum number of recommendations"),
    db: Session = Depends(get_db)
):
    """
    Recommend YouTube videos for a topic
    
    Args:
        topic: Educational topic
        content_summary: Content summary for context
        max_results: Maximum number of recommendations
        db: Database session
        
    Returns:
        List of recommended video dictionaries
    """
    try:
        # Get video recommendations
        videos = youtube_recommender.recommend_videos_for_topic(topic, content_summary, max_results)
        
        return {
            "success": True,
            "data": {
                "topic": topic,
                "recommendations": videos
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))