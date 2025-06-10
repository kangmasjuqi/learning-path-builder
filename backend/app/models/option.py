# backend/app/models/option.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.question import Question # Import Question model

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    question = relationship("Question", back_populates="options", lazy="joined")
    user_answers = relationship("UserAnswer", back_populates="selected_option", lazy="selectin") # For linking user answers to specific options

    def __repr__(self):
        return f"<Option(id={self.id}, text='{self.option_text[:30]}...', is_correct={self.is_correct})>"