from datetime import datetime
from sqlalchemy.orm import Session
from ...database.models import Region, User, Question, QuestionCycle, Assignment
from .cache import get_cached_question, cache_question

def get_cycle_number(cycle_start_date, cycle_duration):
    days_since_start = (datetime.now() - cycle_start_date).days
    cycle_number = (days_since_start // cycle_duration) + 1
    return cycle_number

def assign_questions_for_cycle(user_id: int, cycle_number: int, db: Session):
    # Get user region
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User with id {user_id} not found")
    region = user.region

    # Fetch the cycle config for that region
    cycle_config = db.query(QuestionCycle).filter(QuestionCycle.region_id == region.id).first()
    if not cycle_config:
        raise ValueError(f"No cycle config found for region {region}")

    # Fetch the assigned question for the current cycle which is less than or equal the cycle number
    assigned_question = db.query(Assignment).filter(
        Assignment.region_id == region.id,
        Assignment.cycle_duration <= cycle_number,
    ).order_by(Assignment.cycle_duration.desc()).first()

    # Fetch the question details
    question = db.query(Question).filter(Question.id == assigned_question.question_id).first()
    if not question:
        raise ValueError(f"Question with id {assigned_question.question_id} not found")

    # Cache the question
    cache_question(region.name, cycle_number, question.question_text)

    return question.question_text

def get_questions_for_cycle(cycle_id: int, region_name: str, db: Session):
    questions = db.query(Question).join(Region).filter(
        Question.cycle_id == cycle_id,
        Region.name == region_name
    ).all()

    if not questions:
        raise ValueError(f"No questions found for cycle {cycle_id} and region {region_name}")

    return questions

