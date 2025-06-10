# backend/app/schemas/user_progress.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base UserProgress Schema
class UserProgressBase(BaseModel):
    lesson_id: int
    is_completed: bool = False # Default to false

# Schema for updating user progress (e.g., setting to completed)
class UserProgressUpdate(BaseModel):
    is_completed: bool = True # Only allows setting to True typically

# Schema for UserProgress output
class UserProgressOut(UserProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    last_accessed_at: datetime

    class Config:
        from_attributes = True