from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/pdf_db"
    
    # LLM Services
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # ChromaDB
    chroma_persist_directory: str = "./chroma"
    
    # File Upload
    upload_dir: str = "./uploads/pdfs"
    max_file_size: int = 10485760  # 10MB
    
    # Application
    app_name: str = "RAG Learning Assistant"
    debug: bool = False
    
    # JWT Settings
    secret_key: Optional[str] = "your_secret_key_here"
    algorithm: Optional[str] = "HS256"
    access_token_expire_minutes: Optional[int] = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()