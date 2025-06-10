# backend/app/schemas/lesson.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal, List
from datetime import datetime

# Forward declaration for QuizOut
class QuizOut(BaseModel):
    id: int
    lesson_id: int
    title: str
    class Config:
        from_attributes = True

# Base Lesson Schema
class LessonBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    # Using Literal to restrict content_type values
    content_type: Literal["text", "video", "quiz", "link"]
    content_url: Optional[HttpUrl] = None # Pydantic's HttpUrl for URL validation
    text_content: Optional[str] = None
    order: int = Field(0, ge=0) # Order defaults to 0, must be >= 0

# Schema for Lesson creation (requires course_id)
class LessonCreate(LessonBase):
    course_id: int # Explicitly required during creation

# Schema for Lesson update
class LessonUpdate(LessonBase):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    content_type: Optional[Literal["text", "video", "quiz", "link"]] = None
    content_url: Optional[HttpUrl] = None
    text_content: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)


# Schema for Lesson output
class LessonOut(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    quizzes: List[QuizOut] = [] # Nested quizzes (summary)

    class Config:
        from_attributes = True

# Update the forward declaration in course.py if you haven't already.
# We defined it here as a top-level schema to avoid circular imports.
# Pydantic v2 handles circular imports better if you define them correctly.
# The `LessonOut` definition in `course.py` should match this one.