from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from config.database import DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    pdfs = relationship("PDF", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")

class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    processed = Column(DateTime, nullable=True)
    page_count = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)

    # Relationships
    user = relationship("User", back_populates="pdfs")
    quiz_attempts = relationship("QuizAttempt", back_populates="pdf")
    text_chunks = relationship("TextChunk", back_populates="pdf")

class TextChunk(Base):
    __tablename__ = "text_chunks"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey("pdfs.id"))
    chunk_text = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=False)
    chunk_order = Column(Integer, nullable=False)
    embedding_id = Column(String, nullable=True)

    # Relationships
    pdf = relationship("PDF", back_populates="text_chunks")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey("pdfs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_type = Column(String(20), nullable=False)  # MCQ, SAQ, LAQ
    score = Column(Integer, nullable=True)
    total_questions = Column(Integer, nullable=False)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)
    answers = Column(Text, nullable=True)  # JSON string with user answers

    # Relationships
    pdf = relationship("PDF", back_populates="quiz_attempts")
    user = relationship("User", back_populates="quiz_attempts")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String(100), nullable=False)
    strength_score = Column(Float, nullable=True)  # 0.0 to 1.0
    weakness_score = Column(Float, nullable=True)  # 0.0 to 1.0
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress")

# The following function can be used to create the table in your database.
# You would typically run this once when your application starts.
def create_tables():
    Base.metadata.create_all(bind=engine)