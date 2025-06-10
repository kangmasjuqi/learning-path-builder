# backend/app/api/endpoints/users.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud import crud_user
from app.api.deps import get_current_active_user, get_current_educator # Import dependencies for authorization
from app.models.user import User as DBUser # Alias to avoid conflict with schemas.UserOut

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Register New User")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registers a new user (student or educator).
    """
    db_user_by_email = crud_user.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user_by_username = crud_user.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    return crud_user.create_user(db=db, user=user)

@router.get("/me", response_model=UserOut, summary="Get Current User Profile")
def read_users_me(
    current_user: DBUser = Depends(get_current_active_user)
):
    """
    Retrieves the profile of the currently authenticated user.
    """
    return current_user

@router.put("/me", response_model=UserOut, summary="Update Current User Profile")
def update_users_me(
    user_in: UserUpdate,
    current_user: DBUser = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Updates the profile of the currently authenticated user.
    """
    return crud_user.update_user(db=db, db_user=current_user, user_in=user_in)

# --- Admin/Educator Only Endpoints (Example) ---
@router.get("/", response_model=List[UserOut], summary="Get All Users (Admin/Educator Only)")
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # This endpoint is restricted to educators
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Retrieves a list of all users. Accessible only by educators.
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserOut, summary="Get User by ID (Admin/Educator Only)")
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Retrieves a specific user by ID. Accessible only by educators.
    """
    user = crud_user.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user