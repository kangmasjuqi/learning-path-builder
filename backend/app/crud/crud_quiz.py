# backend/app/crud/crud_quiz.py
from sqlalchemy.orm import Session
from app.models.quiz import Quiz
from app.schemas.quiz import QuizCreate, QuizUpdate

def get_quiz(db: Session, quiz_id: int):
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()

def get_quiz_by_lesson_id(db: Session, lesson_id: int):
    # A lesson should typically only have one quiz
    return db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()

def create_quiz(db: Session, quiz: QuizCreate):
    db_quiz = Quiz(**quiz.model_dump())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def update_quiz(db: Session, db_quiz: Quiz, quiz_in: QuizUpdate):
    for key, value in quiz_in.model_dump(exclude_unset=True).items():
        setattr(db_quiz, key, value)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def delete_quiz(db: Session, quiz_id: int):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
        return True
    return False