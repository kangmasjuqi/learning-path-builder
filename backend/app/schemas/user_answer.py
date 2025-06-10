# backend/app/schemas/user_answer.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base UserAnswer Schema
class UserAnswerBase(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None # For MCQ
    user_answer_text: Optional[str] = None # For ShortAnswer

# Schema for UserAnswer submission (doesn't include user_id, that's from JWT)
class UserAnswerCreate(UserAnswerBase):
    pass # No additional fields needed beyond base for submission

# Schema for UserAnswer output
class UserAnswerOut(UserAnswerBase):
    id: int
    user_id: int
    is_correct: Optional[bool] = None # Graded by the system or None if not yet
    answered_at: datetime

    class Config:
        from_attributes = True