from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="users")

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="region")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    question_text = Column(String)
    region_id = Column(Integer, ForeignKey("regions.id"))
    cycle_id = Column(Integer, ForeignKey("question_cycles.id"))

class QuestionCycle(Base):
    __tablename__ = "question_cycles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"))
    duration = Column(Integer, default=7) # in days
    start_date = Column(Date, default=datetime.now)

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    cycle_duration = Column(Integer, default=7)
    assigned_date = Column(DateTime)
