from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from .models import Assignment, Base, Question, QuestionCycle, Region, User

DB_URL = "sqlite:///./stroll.db"
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite://") else {}
engine = create_engine(DB_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def try_migration():
    """ Try to inspect/migrate tables to the database on startup. """
    from sqlalchemy import inspect

    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    supported_tables = ["regions", "questions", "question_cycles", "users", "assignments"]
    if not all(table in table_names for table in supported_tables):
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(e)

def seed_db(db: Session):
    # Seed the DB with questions and a user
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == "fantasticbob").first()
    if existing_user:
        print("Seeding skipped because user already exists")
        return

    # Create region first
    new_region1 = Region(name="us-east-1")
    new_region2 = Region(name="us-east-2")
    db.add(new_region1)
    db.add(new_region2)
    db.commit()

    # Create user
    new_user = User(username="fantasticbob", hashed_password="password", region_id=new_region1.id)
    db.add(new_user)
    db.commit()

    # Create question cycle
    new_cycle1 = QuestionCycle(region_id=new_region1.id)
    new_cycle2 = QuestionCycle(region_id=new_region2.id)
    db.add(new_cycle1)
    db.add(new_cycle2)
    db.commit()

    # Create questions
    new_question1 = Question(question_text="Question 1", region_id=new_region1.id, cycle_id=new_cycle1.id)
    new_question2 = Question(question_text="Question 2", region_id=new_region1.id, cycle_id=new_cycle1.id)
    new_question3 = Question(question_text="Question 3", region_id=new_region2.id, cycle_id=new_cycle2.id)
    new_question4 = Question(question_text="Question 4", region_id=new_region2.id, cycle_id=new_cycle2.id)
    new_question5 = Question(question_text="Question 5", region_id=new_region1.id, cycle_id=new_cycle1.id)
    new_question6 = Question(question_text="Question 6", region_id=new_region1.id, cycle_id=new_cycle1.id)
    new_question7 = Question(question_text="Question 7", region_id=new_region2.id, cycle_id=new_cycle2.id)
    new_question8 = Question(question_text="Question 8", region_id=new_region2.id, cycle_id=new_cycle2.id)

    # Assign questions to cycles
    new_assignment1 = Assignment(question_id=1, region_id=new_region1.id, assigned_date=datetime.now())
    new_assignment2 = Assignment(question_id=2, region_id=new_region1.id, assigned_date=datetime.now()-timedelta(days=1))
    new_assignment3 = Assignment(question_id=3, region_id=new_region2.id, assigned_date=datetime.now())
    new_assignment4 = Assignment(question_id=4, region_id=new_region2.id, assigned_date=datetime.now()-timedelta(days=1))
    new_assignment5 = Assignment(question_id=5, region_id=new_region1.id, assigned_date=datetime.now())
    new_assignment6 = Assignment(question_id=6, region_id=new_region1.id, assigned_date=datetime.now()-timedelta(days=1))
    new_assignment7 = Assignment(question_id=7, region_id=new_region2.id, assigned_date=datetime.now())
    new_assignment8 = Assignment(question_id=8, region_id=new_region2.id, assigned_date=datetime.now()-timedelta(days=1))

    db.add(new_question1)
    db.add(new_question2)
    db.add(new_question3)
    db.add(new_question4)
    db.add(new_question5)
    db.add(new_question6)
    db.add(new_question7)
    db.add(new_question8)
    db.commit()

    db.add(new_assignment1)
    db.add(new_assignment2)
    db.add(new_assignment3)
    db.add(new_assignment4)
    db.add(new_assignment5)
    db.add(new_assignment6)
    db.add(new_assignment7)
    db.add(new_assignment8)
    db.commit()







