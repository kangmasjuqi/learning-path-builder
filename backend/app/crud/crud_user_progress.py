# backend/app/crud/crud_user_progress.py
from sqlalchemy.orm import Session
from app.models.user_progress import UserProgress
from app.schemas.user_progress import UserProgressUpdate
from datetime import datetime
from sqlalchemy import and_

def get_user_progress(db: Session, user_progress_id: int):
    return db.query(UserProgress).filter(UserProgress.id == user_progress_id).first()

def get_user_progress_for_lesson(db: Session, user_id: int, lesson_id: int):
    return db.query(UserProgress).filter(
        and_(UserProgress.user_id == user_id, UserProgress.lesson_id == lesson_id)
    ).first()

def get_user_progress_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(UserProgress).filter(UserProgress.user_id == user_id).offset(skip).limit(limit).all()

def create_or_update_user_progress(db: Session, user_id: int, lesson_id: int, is_completed: bool = False):
    db_progress = get_user_progress_for_lesson(db, user_id, lesson_id)
    if db_progress:
        # Update existing progress
        db_progress.is_completed = is_completed
        if is_completed and not db_progress.completed_at: # Set completion time only if just completed
            db_progress.completed_at = datetime.now()
        elif not is_completed: # If marked incomplete, clear completed_at
            db_progress.completed_at = None
    else:
        # Create new progress
        db_progress = UserProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            is_completed=is_completed,
            completed_at=datetime.now() if is_completed else None
        )
        db.add(db_progress)

    db.commit()
    db.refresh(db_progress)
    return db_progress

def update_user_progress(db: Session, db_progress: UserProgress, progress_in: UserProgressUpdate):
    # This function assumes you already have the db_progress object
    # and only allows updating the `is_completed` status.
    db_progress.is_completed = progress_in.is_completed
    if progress_in.is_completed and not db_progress.completed_at:
        db_progress.completed_at = datetime.now()
    elif not progress_in.is_completed:
        db_progress.completed_at = None

    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress