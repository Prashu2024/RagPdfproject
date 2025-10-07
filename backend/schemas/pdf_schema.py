from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PDFBase(BaseModel):
    filename: str
    filepath: str

class PDFCreate(PDFBase):
    user_id: int

class PDF(PDFBase):
    id: int
    user_id: int
    uploaded_at: datetime
    processed: Optional[datetime] = None
    page_count: Optional[int] = None
    file_size: Optional[int] = None
    
    class Config:
        from_attributes = True

class TextChunkBase(BaseModel):
    pdf_id: int
    chunk_text: str
    page_number: int
    chunk_order: int

class TextChunkCreate(TextChunkBase):
    pass

class TextChunk(TextChunkBase):
    id: int
    embedding_id: Optional[str] = None
    
    class Config:
        from_attributes = True

class QuizAttemptBase(BaseModel):
    pdf_id: int
    quiz_type: str
    total_questions: int

class QuizAttemptCreate(QuizAttemptBase):
    pass

class QuizAttempt(QuizAttemptBase):
    id: int
    user_id: int
    score: Optional[int] = None
    completed_at: datetime
    answers: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserProgressBase(BaseModel):
    user_id: int
    topic: str
    strength_score: Optional[float] = None
    weakness_score: Optional[float] = None

class UserProgressCreate(UserProgressBase):
    pass

class UserProgress(UserProgressBase):
    id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

class QuizQuestion(BaseModel):
    question: str
    type: str  # MCQ, SAQ, LAQ
    difficulty: str  # Easy, Medium, Hard
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]

class QuizAnswer(BaseModel):
    question_id: int
    answer: str

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[QuizAnswer]

class QuizResult(BaseModel):
    quiz_id: str
    score: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    answers: List[dict]