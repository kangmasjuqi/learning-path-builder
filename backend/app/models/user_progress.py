# backend/app/models/user_progress.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import User
from app.models.lesson import Lesson

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True) # Only set if is_completed is True
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Ensure unique constraint for user_id and lesson_id
    # This prevents a user from having multiple progress entries for the same lesson
    # You can add this directly to the table args or via migration later
    # __table_args__ = (UniqueConstraint('user_id', 'lesson_id', name='_user_lesson_uc'),)


    # Relationships
    user = relationship("User", back_populates="progress", lazy="joined")
    lesson = relationship("Lesson", back_populates="user_progress", lazy="joined")

    def __repr__(self):
        return f"<UserProgress(id={self.id}, user_id={self.user_id}, lesson_id={self.lesson_id}, completed={self.is_completed})>"