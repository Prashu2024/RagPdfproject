
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import pdf_routes, quiz_routes, chat_routes, progress_routes
from config.database import create_tables
from config.settings import settings

# Create database tables
create_tables()

app = FastAPI(
    title=settings.app_name,
    description="A RAG-based learning assistant for school students",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdf_routes.router, prefix="/api/pdfs", tags=["PDFs"])
app.include_router(quiz_routes.router, prefix="/api/quizzes", tags=["Quizzes"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])
app.include_router(progress_routes.router, prefix="/api/progress", tags=["Progress"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the RAG-based learning assistant!",
        "version": "1.0.0",
        "features": [
            "PDF upload and processing",
            "Quiz generation (MCQ, SAQ, LAQ)",
            "RAG-based Q&A",
            "Progress tracking",
            "YouTube recommendations"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.app_name}
