# backend/app/api/endpoints/quizzes.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.quiz import QuizCreate, QuizOut, QuizUpdate
from app.schemas.question import QuestionCreate, QuestionOut, QuestionWithAnswersOut, OptionCreate, QuestionUpdate
from app.crud import crud_quiz, crud_lesson, crud_question
from app.api.deps import get_current_educator
from app.models.user import User as DBUser

router = APIRouter()

@router.post("/", response_model=QuizOut, status_code=status.HTTP_201_CREATED, summary="Create New Quiz")
def create_quiz(
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Creates a new quiz for a specific lesson. Only accessible by the lesson's course educator.
    A lesson can only have one quiz.
    """
    lesson = crud_lesson.get_lesson(db, lesson_id=quiz.lesson_id)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    if lesson.course.educator_id != current_educator.id: # Access course through lesson relationship
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create quiz for this lesson")

    existing_quiz = crud_quiz.get_quiz_by_lesson_id(db, lesson_id=quiz.lesson_id)
    if existing_quiz:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lesson already has a quiz.")

    return crud_quiz.create_quiz(db=db, quiz=quiz)

@router.get("/{quiz_id}", response_model=QuizOut, summary="Get Quiz by ID (Student View)")
def read_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific quiz by its ID, including its questions (without correct answers for students).
    """
    quiz = crud_quiz.get_quiz(db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    return quiz

@router.get("/{quiz_id}/with-answers", response_model=QuizOut, summary="Get Quiz by ID (Educator View)")
def read_quiz_with_answers(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Retrieves a specific quiz by its ID, including questions with correct answers.
    Accessible only by the quiz's owning course educator.
    """
    quiz = crud_quiz.get_quiz(db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    if quiz.lesson.course.educator_id != current_educator.id: # Access course through lesson relationship
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view answers for this quiz")

    # Dynamically set the response model for questions to include answers
    quiz_out_with_answers = QuizOut.model_validate(quiz.model_dump())
    for q_idx, question in enumerate(quiz.questions):
        options_with_correctness = [
            OptionCreate.model_validate(opt.model_dump()) for opt in question.options
        ]
        quiz_out_with_answers.questions[q_idx] = QuestionWithAnswersOut(
            **question.model_dump(),
            options=options_with_correctness # Use the schema that includes is_correct
        )
    return quiz_out_with_answers

@router.put("/{quiz_id}", response_model=QuizOut, summary="Update Quiz")
def update_quiz(
    quiz_id: int,
    quiz_in: QuizUpdate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Updates an existing quiz. Only accessible by the lesson's course educator.
    """
    db_quiz = crud_quiz.get_quiz(db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    if db_quiz.lesson.course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this quiz")

    return crud_quiz.update_quiz(db=db, db_quiz=db_quiz, quiz_in=quiz_in)

@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Quiz")
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Deletes a quiz. Only accessible by the lesson's course educator.
    """
    db_quiz = crud_quiz.get_quiz(db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    if db_quiz.lesson.course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this quiz")

    if not crud_quiz.delete_quiz(db=db, quiz_id=quiz_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete quiz")
    return {"message": "Quiz deleted successfully"}

# --- Question Endpoints ---
@router.post("/{quiz_id}/questions/", response_model=QuestionOut, status_code=status.HTTP_201_CREATED, summary="Add Question to Quiz")
def create_question_for_quiz(
    quiz_id: int,
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Adds a new question to a quiz. Only accessible by the quiz's owning educator.
    """
    db_quiz = crud_quiz.get_quiz(db, quiz_id=quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    if db_quiz.lesson.course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add questions to this quiz")

    # Override quiz_id from path
    question.quiz_id = quiz_id
    return crud_question.create_question(db=db, question=question)

@router.put("/questions/{question_id}", response_model=QuestionOut, summary="Update Question")
def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Updates an existing question. Only accessible by the owning quiz's educator.
    """
    db_question = crud_question.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if db_question.quiz.lesson.course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this question")

    return crud_question.update_question(db=db, db_question=db_question, question_in=question_in)

@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Question")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_educator: DBUser = Depends(get_current_educator)
):
    """
    Deletes a question. Only accessible by the owning quiz's educator.
    """
    db_question = crud_question.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if db_question.quiz.lesson.course.educator_id != current_educator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this question")

    if not crud_question.delete_question(db=db, question_id=question_id):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete question")
    return {"message": "Question deleted successfully"}

# TODO: Add endpoints for managing options under a question if needed for advanced editing