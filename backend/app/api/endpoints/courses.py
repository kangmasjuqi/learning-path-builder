# backend/app/api/endpoints/courses.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate
from app.crud import crud_course
from app.api.deps import get_current_active_user, get_current_educator
from app.models.user import User as DBUser # Alias for current_user type hint

router = APIRouter()

@router.post("/", response_model=CourseOut, status_code=status.HTTP_201_CREATED, summary="Create New Course")
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator) # Only educators can create courses
):
    """
    Creates a new learning course. Only accessible by educators.
    """
    return crud_course.create_course(db=db, course=course, educator_id=current_educator.id)

@router.get("/", response_model=List[CourseOut], summary="Get All Courses")
def read_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieves a list of all available courses. Accessible by any authenticated user.
    """
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses

@router.get("/{course_id}", response_model=CourseOut, summary="Get Course by ID")
def read_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific course by its ID, including its lessons.
    """
    course = crud_course.get_course(db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseOut, summary="Update Course")
def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator) # Only educators can update courses
):
    """
    Updates an existing course. Only accessible by the course's educator.
    """
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if db_course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this course")

    return crud_course.update_course(db=db, db_course=db_course, course_in=course_in)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Course")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator) # Only educators can delete courses
):
    """
    Deletes a course. Only accessible by the course's educator.
    """
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if db_course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this course")

    if not crud_course.delete_course(db=db, course_id=course_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete course")
    return {"message": "Course deleted successfully"}