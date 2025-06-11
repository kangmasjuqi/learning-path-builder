# backend/app/core/jwt.py
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.config import settings # Our configuration with SECRET_KEY and ALGORITHM
from pydantic import BaseModel
from app.models.user import User as DBUser

# Token payload structure (optional, but good for clarity)
class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = [] # For role-based authorization later
    id: Optional[int] = None
    email: Optional[str] = None
    is_educator: Optional[bool] = None
    is_active: Optional[bool] = None

def create_access_token(user: DBUser, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token."""
    to_encode = {
        "sub": user.username,
        "id": user.id,
        "email": user.email,
        "is_educator": user.is_educator,
        "is_active": user.is_active,
        "scopes": ["user", "educator"] if user.is_educator else ["user"],
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException):
    """Verifies a JWT token and returns the payload."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub") # 'sub' is the subject, usually username
        if username is None:
            raise credentials_exception
        # Optionally, extract scopes/roles
        # token_data = TokenData(username=username, scopes=payload.get("scopes", []))
        return payload # Return full payload for now, can be refined to TokenData
    except JWTError:
        raise credentials_exception