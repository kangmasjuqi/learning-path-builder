# backend/app/schemas/quiz.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Forward declaration for QuestionOut to resolve circular imports
class QuestionOut(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    question_type: str
    class Config:
        from_attributes = True

# Base Quiz Schema
class QuizBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

# Schema for Quiz creation (requires lesson_id)
class QuizCreate(QuizBase):
    lesson_id: int # Explicitly required during creation

# Schema for Quiz update
class QuizUpdate(QuizBase):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None

# Schema for Quiz output
class QuizOut(QuizBase):
    id: int
    lesson_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    questions: List[QuestionOut] = [] # Nested questions (summary)

    class Config:
        from_attributes = True