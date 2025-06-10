# backend/app/schemas/question.py
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

# Forward declaration for OptionOut and UserAnswerOut
class OptionOut(BaseModel):
    id: int
    question_id: int
    option_text: str
    # Do NOT include is_correct here for standard student output
    class Config:
        from_attributes = True

class OptionWithCorrectnessOut(OptionOut):
    is_correct: bool # For educator/admin view

class UserAnswerOut(BaseModel):
    id: int
    user_id: int
    question_id: int
    is_correct: Optional[bool] = None # Graded status
    answered_at: datetime
    class Config:
        from_attributes = True

# Base Question Schema
class QuestionBase(BaseModel):
    question_text: str = Field(..., min_length=5)
    question_type: Literal["MCQ", "TrueFalse", "ShortAnswer"] = "MCQ"

# Schema for Option creation (for MCQ questions)
class OptionCreate(BaseModel):
    option_text: str = Field(..., min_length=1)
    is_correct: bool = False

# Schema for Question creation (includes options for MCQ)
class QuestionCreate(QuestionBase):
    quiz_id: int
    options: Optional[List[OptionCreate]] = None # For MCQ type questions

# Schema for Question update
class QuestionUpdate(QuestionBase):
    question_text: Optional[str] = Field(None, min_length=5)
    question_type: Optional[Literal["MCQ", "TrueFalse", "ShortAnswer"]] = None
    # Note: Updating options usually involves separate endpoints or more complex logic
    # For simplicity, we won't include options directly in QuestionUpdate

# Schema for Question output (for students - hides correct answers)
class QuestionOut(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    options: List[OptionOut] = [] # Student view of options (no correctness)

    class Config:
        from_attributes = True

# Schema for Question output (for educators/admins - shows correct answers)
class QuestionWithAnswersOut(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    options: List[OptionWithCorrectnessOut] = [] # Educator view of options

    class Config:
        from_attributes = True