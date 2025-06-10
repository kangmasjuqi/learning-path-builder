# backend/app/api/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import verify_token
from app.crud import crud_user # Import crud_user
from app.models.user import User # Import User model

# OAuth2 scheme for token retrieval from headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # "token" is the endpoint for getting tokens

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Dependency to get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = crud_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to get the current active authenticated user."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_educator(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Dependency to get the current authenticated educator."""
    if not current_user.is_educator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user