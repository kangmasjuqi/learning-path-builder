# backend/app/models/user_answer.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import User
from app.models.question import Question
from app.models.option import Option

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("options.id"), nullable=True) # For MCQ answers
    user_answer_text = Column(Text, nullable=True) # For ShortAnswer or other text-based answers
    is_correct = Column(Boolean, nullable=True) # True/False/None (if not yet graded)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", lazy="joined")
    question = relationship("Question", back_populates="user_answers", lazy="joined")
    selected_option = relationship("Option", back_populates="user_answers", lazy="joined")

    def __repr__(self):
        return f"<UserAnswer(id={self.id}, user_id={self.user_id}, question_id={self.question_id}, is_correct={self.is_correct})>"