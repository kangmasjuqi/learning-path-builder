# backend/app/models/question.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.quiz import Quiz # Import Quiz model

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    # e.g., 'MCQ', 'TrueFalse', 'ShortAnswer'
    question_type = Column(String, nullable=False, default="MCQ")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="questions", lazy="joined")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan", lazy="joined") # For MCQ
    user_answers = relationship("UserAnswer", back_populates="question", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self):
        return f"<Question(id={self.id}, text='{self.question_text[:30]}...', quiz_id={self.quiz_id})>"