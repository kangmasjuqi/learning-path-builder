# backend/app/api/endpoints/progress.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_progress import UserProgressOut
from app.schemas.user_answer import UserAnswerCreate, UserAnswerOut
from app.crud import crud_user_progress, crud_user_answer, crud_lesson, crud_quiz, crud_question
from app.api.deps import get_current_active_user
from app.models.user import User as DBUser

router = APIRouter()

@router.post("/lessons/{lesson_id}/complete", response_model=UserProgressOut, summary="Mark Lesson as Complete")
def mark_lesson_complete(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """
    Marks a specific lesson as completed for the current user.
    If a quiz exists for the lesson, ensure it's completed first.
    """
    lesson = crud_lesson.get_lesson(db, lesson_id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    # Optional: Check if there's an associated quiz and if it's completed
    quiz = crud_quiz.get_quiz_by_lesson_id(db, lesson_id=lesson_id)
    if quiz:
        # Check if all questions in the quiz have been answered by the user
        all_questions = crud_question.get_questions_by_quiz(db, quiz_id=quiz.id)
        if all_questions: # Only check if quiz has questions
            for question in all_questions:
                user_answer = crud_user_answer.get_user_answer_for_question(db, current_user.id, question.id)
                if not user_answer or user_answer.is_correct is None: # Assuming `is_correct` being None means not graded/answered
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Please complete the associated quiz before marking the lesson complete."
                    )
                # For a stricter check, you might require is_correct == True
                # if user_answer.is_correct is not True:
                #     raise HTTPException(...)

    return crud_user_progress.create_or_update_user_progress(
        db=db, user_id=current_user.id, lesson_id=lesson_id, is_completed=True
    )

@router.get("/me", response_model=List[UserProgressOut], summary="Get Current User's Progress")
def get_my_progress(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """
    Retrieves the progress of the current authenticated user across all lessons.
    """
    return crud_user_progress.get_user_progress_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/answers/", response_model=UserAnswerOut, status_code=status.HTTP_201_CREATED, summary="Submit Quiz Answer")
def submit_answer(
    answer: UserAnswerCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """
    Submits an answer to a quiz question for the current user.
    Will automatically grade MCQ answers.
    """
    # Ensure the question exists and belongs to a quiz within a lesson
    question = crud_question.get_question(db, question_id=answer.question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    # Optional: Check if user already answered this question and prevent re-submission
    existing_answer = crud_user_answer.get_user_answer_for_question(db, current_user.id, answer.question_id)
    if existing_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already answered this question.")


    return crud_user_answer.create_user_answer(db=db, user_answer=answer, user_id=current_user.id)

@router.get("/answers/me", response_model=List[UserAnswerOut], summary="Get Current User's Answers")
def get_my_answers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """
    Retrieves all answers submitted by the current authenticated user.
    """
    return crud_user_answer.get_user_answers_by_user(db, user_id=current_user.id, skip=skip, limit=limit)