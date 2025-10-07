import pytest
import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "features" in data

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data

def test_pdf_upload_missing_file():
    """Test PDF upload without file"""
    response = client.post("/api/pdfs/upload")
    assert response.status_code == 422  # Validation error

def test_quiz_generation_invalid_pdf():
    """Test quiz generation with invalid PDF ID"""
    response = client.post("/api/quizzes/generate", json={
        "pdf_id": 99999,  # Non-existent PDF
        "quiz_type": "MCQ",
        "num_questions": 5
    })
    assert response.status_code == 422  # Will fail due to database constraint

def test_chat_ask_endpoint():
    """Test the chat ask endpoint"""
    response = client.post("/api/chat/ask", json={
        "question": "What is learning?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data
    assert "question" in data["data"]
    assert "answer" in data["data"]

def test_progress_user_endpoint():
    """Test progress endpoint for user"""
    response = client.get("/api/progress/user/1")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data

def test_quiz_statistics():
    """Test quiz statistics endpoint"""
    response = client.get("/api/quizzes/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data

def test_overall_stats():
    """Test overall platform statistics"""
    response = client.get("/api/progress/stats/overview")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data

def test_invalid_endpoint():
    """Test invalid endpoint"""
    response = client.get("/api/invalid-endpoint")
    assert response.status_code == 404

def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers