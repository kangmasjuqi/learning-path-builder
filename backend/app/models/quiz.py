# backend/app/models/quiz.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.lesson import Lesson # Import Lesson model

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, unique=True) # One quiz per lesson
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lesson = relationship("Lesson", back_populates="quizzes", lazy="joined")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', lesson_id={self.lesson_id})>"