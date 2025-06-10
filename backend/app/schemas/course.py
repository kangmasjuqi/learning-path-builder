# backend/app/schemas/course.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Forward declaration for LessonOut to resolve circular imports
# when CourseOut needs to reference LessonOut.
# This is a common pattern in Pydantic with deeply nested relationships.
class LessonOut(BaseModel):
    id: int
    course_id: int
    title: str
    content_type: str
    order: int
    created_at: datetime
    # Add other fields as needed for a summarized lesson view
    # For full lesson details, you might need a separate endpoint.
    class Config:
        from_attributes = True

# Base Course Schema
class CourseBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None

# Schema for Course creation
class CourseCreate(CourseBase):
    pass # No additional fields needed beyond CourseBase for creation

# Schema for Course update
class CourseUpdate(CourseBase):
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = None

# Schema for Course output (includes educator_id and potentially lessons)
class CourseOut(CourseBase):
    id: int
    educator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    lessons: List[LessonOut] = [] # Nested lessons (summary)

    class Config:
        from_attributes = True