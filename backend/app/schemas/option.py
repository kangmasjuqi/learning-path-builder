# backend/app/schemas/option.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base Option Schema
class OptionBase(BaseModel):
    option_text: str = Field(..., min_length=1)

# Schema for Option creation (requires question_id, includes correctness)
class OptionCreate(OptionBase):
    question_id: int
    is_correct: bool = False

# Schema for Option update
class OptionUpdate(OptionBase):
    option_text: Optional[str] = Field(None, min_length=1)
    is_correct: Optional[bool] = None

# Schema for Option output (standard view, without correctness)
class OptionOut(OptionBase):
    id: int
    question_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schema for Option output including correctness (for educators/admin)
class OptionWithCorrectnessOut(OptionOut):
    is_correct: bool

    class Config:
        from_attributes = True