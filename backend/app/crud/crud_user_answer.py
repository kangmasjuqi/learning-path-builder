# backend/app/crud/crud_user_answer.py
from sqlalchemy.orm import Session
from app.models.user_answer import UserAnswer
from app.schemas.user_answer import UserAnswerCreate
from app.models.question import Question # For grading logic
from app.models.option import Option # For grading logic

def get_user_answer(db: Session, user_answer_id: int):
    return db.query(UserAnswer).filter(UserAnswer.id == user_answer_id).first()

def get_user_answers_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(UserAnswer).filter(UserAnswer.user_id == user_id).offset(skip).limit(limit).all()

def get_user_answer_for_question(db: Session, user_id: int, question_id: int):
    return db.query(UserAnswer).filter(
        UserAnswer.user_id == user_id,
        UserAnswer.question_id == question_id
    ).first()

def create_user_answer(db: Session, user_answer: UserAnswerCreate, user_id: int):
    # Retrieve the question to determine grading logic
    question = db.query(Question).filter(Question.id == user_answer.question_id).first()
    if not question:
        raise ValueError("Question not found")

    is_correct = None # Default to None, indicating not yet graded or irrelevant for type

    if question.question_type == "MCQ":
        if user_answer.selected_option_id:
            selected_option = db.query(Option).filter(
                Option.id == user_answer.selected_option_id,
                Option.question_id == question.id
            ).first()
            if selected_option:
                is_correct = selected_option.is_correct
    elif question.question_type == "TrueFalse":
        # Assuming 'True' or 'False' as text_content
        # You might need a more sophisticated logic here, e.g., an 'answer' field on Question
        pass # Placeholder for grading True/False
    elif question.question_type == "ShortAnswer":
        pass # Short answer grading is usually manual or regex-based, not automated here

    db_user_answer = UserAnswer(
        user_id=user_id,
        question_id=user_answer.question_id,
        selected_option_id=user_answer.selected_option_id,
        user_answer_text=user_answer.user_answer_text,
        is_correct=is_correct # Set based on automatic grading
    )
    db.add(db_user_answer)
    db.commit()
    db.refresh(db_user_answer)
    return db_user_answer