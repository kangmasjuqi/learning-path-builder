# backend/app/crud/crud_question.py
from sqlalchemy.orm import Session
from app.models.question import Question
from app.models.option import Option
from app.schemas.question import QuestionCreate, QuestionUpdate, OptionCreate

def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()

def get_questions_by_quiz(db: Session, quiz_id: int, skip: int = 0, limit: int = 100):
    return db.query(Question).filter(Question.quiz_id == quiz_id).offset(skip).limit(limit).all()

def create_question(db: Session, question: QuestionCreate):
    question_dict = question.model_dump()
    options_data = question_dict.pop("options", []) # Extract options if present

    db_question = Question(**question_dict)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Add options if provided (only for MCQ typically)
    if db_question.question_type == "MCQ" and options_data:
        for opt_data in options_data:
            db_option = Option(question_id=db_question.id, **opt_data)
            db.add(db_option)
        db.commit()
        db.refresh(db_question) # Refresh again to load new options relationship

    return db_question

def update_question(db: Session, db_question: Question, question_in: QuestionUpdate):
    for key, value in question_in.model_dump(exclude_unset=True).items():
        setattr(db_question, key, value)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
        return True
    return False

# CRUD for Options (can be separate or part of question CRUD)
def create_option(db: Session, option: OptionCreate, question_id: int):
    db_option = Option(**option.model_dump(), question_id=question_id)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

def get_option(db: Session, option_id: int):
    return db.query(Option).filter(Option.id == option_id).first()

def update_option(db: Session, db_option: Option, option_in: OptionCreate): # Re-use OptionCreate for update if no dedicated update schema
    for key, value in option_in.model_dump(exclude_unset=True).items():
        setattr(db_option, key, value)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

def delete_option(db: Session, option_id: int):
    db_option = db.query(Option).filter(Option.id == option_id).first()
    if db_option:
        db.delete(db_option)
        db.commit()
        return True
    return False