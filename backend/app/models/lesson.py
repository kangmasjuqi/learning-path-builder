# backend/app/models/lesson.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.course import Course # Import Course model for relationship

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, index=True, nullable=False)
    # 'text', 'video', 'quiz', 'link' - allows for future extensibility
    content_type = Column(String, nullable=False)
    content_url = Column(String, nullable=True) # For video links, external articles
    text_content = Column(Text, nullable=True) # For inline text content
    order = Column(Integer, default=0, nullable=False) # Order within a course
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    course = relationship("Course", back_populates="lessons", lazy="joined")
    quizzes = relationship("Quiz", back_populates="lesson", cascade="all, delete-orphan", lazy="joined")
    user_progress = relationship("UserProgress", back_populates="lesson", cascade="all, delete-orphan", lazy="selectin") # Use selectin for efficient loading of many-to-many-like relationship

    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}', course_id={self.course_id})>"