# backend/app/crud/crud_course.py
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def get_courses_by_educator(db: Session, educator_id: int, skip: int = 0, limit: int = 100):
    return db.query(Course).filter(Course.educator_id == educator_id).offset(skip).limit(limit).all()

def create_course(db: Session, course: CourseCreate, educator_id: int):
    db_course = Course(**course.model_dump(), educator_id=educator_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, db_course: Course, course_in: CourseUpdate):
    for key, value in course_in.model_dump(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False