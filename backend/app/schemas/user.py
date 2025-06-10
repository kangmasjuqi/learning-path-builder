# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Base User Schema (common attributes)
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_educator: bool = False # Default to False

# Schema for User creation (includes password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Schema for User update (all fields optional, allows partial updates)
class UserUpdate(UserBase):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_educator: Optional[bool] = None

# Schema for User output (excludes sensitive fields like hashed_password)
# This will be used as FastAPI's `response_model`
class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Pydantic V2 equivalent of `orm_mode = True` for SQLAlchemy compatibility