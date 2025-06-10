# backend/app/models/course.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import User # Import User model for relationship

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    educator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    educator = relationship("User", back_populates="courses", lazy="joined")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', educator_id={self.educator_id})>"