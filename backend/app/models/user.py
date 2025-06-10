# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_educator = Column(Boolean, default=False) # New field to differentiate roles
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (define these as we add other models)
    courses = relationship("Course", back_populates="educator", lazy="joined") # Educator's courses
    progress = relationship("UserProgress", back_populates="user", lazy="joined") # Student's progress

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_educator={self.is_educator})>"