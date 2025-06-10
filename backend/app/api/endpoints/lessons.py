# backend/app/api/endpoints/lessons.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lesson import LessonCreate, LessonOut, LessonUpdate
from app.crud import crud_lesson, crud_course # Need crud_course to check course existence/ownership
from app.api.deps import get_current_educator
from app.models.user import User as DBUser

router = APIRouter()

@router.post("/", response_model=LessonOut, status_code=status.HTTP_201_CREATED, summary="Create New Lesson")
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Creates a new lesson for a specific course. Only accessible by the course's educator.
    """
    course = crud_course.get_course(db, course_id=lesson.course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add lessons to this course")

    return crud_lesson.create_lesson(db=db, lesson=lesson)

@router.get("/by-course/{course_id}", response_model=List[LessonOut], summary="Get Lessons by Course ID")
def read_lessons_by_course(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieves all lessons for a given course, ordered by their 'order' field.
    """
    course = crud_course.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    lessons = crud_lesson.get_lessons_by_course(db, course_id=course_id, skip=skip, limit=limit)
    return lessons

@router.get("/{lesson_id}", response_model=LessonOut, summary="Get Lesson by ID")
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific lesson by its ID.
    """
    lesson = crud_lesson.get_lesson(db, lesson_id=lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson

@router.put("/{lesson_id}", response_model=LessonOut, summary="Update Lesson")
def update_lesson(
    lesson_id: int,
    lesson_in: LessonUpdate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Updates an existing lesson. Only accessible by the owning course's educator.
    """
    db_lesson = crud_lesson.get_lesson(db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    # Check if the current educator owns the course associated with the lesson
    course = crud_course.get_course(db, course_id=db_lesson.course_id)
    if not course or course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this lesson")

    return crud_lesson.update_lesson(db=db, db_lesson=db_lesson, lesson_in=lesson_in)

@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Lesson")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Deletes a lesson. Only accessible by the owning course's educator.
    """
    db_lesson = crud_lesson.get_lesson(db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    # Check if the current educator owns the course associated with the lesson
    course = crud_course.get_course(db, course_id=db_lesson.course_id)
    if not course or course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this lesson")

    if not crud_lesson.delete_lesson(db=db, lesson_id=lesson_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete lesson")
    return {"message": "Lesson deleted successfully"}