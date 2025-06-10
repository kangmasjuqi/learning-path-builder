# backend/app/crud/crud_lesson.py
from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate

def get_lesson(db: Session, lesson_id: int):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()

def get_lessons_by_course(db: Session, course_id: int, skip: int = 0, limit: int = 100):
    return db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).offset(skip).limit(limit).all()

def create_lesson(db: Session, lesson: LessonCreate):
    db_lesson = Lesson(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def update_lesson(db: Session, db_lesson: Lesson, lesson_in: LessonUpdate):
    for key, value in lesson_in.model_dump(exclude_unset=True).items():
        setattr(db_lesson, key, value)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def delete_lesson(db: Session, lesson_id: int):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if db_lesson:
        db.delete(db_lesson)
        db.commit()
        return True
    return False