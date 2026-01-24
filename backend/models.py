from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, index=True)

    quizzes = relationship("Quiz", back_populates="author")
    results = relationship("Result", back_populates="user")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    topic = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    difficulty = Column(Integer)

    author = relationship("User", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")
    results = relationship("Result", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    text = Column(String, index=True)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_answer = Column(String)  # "A", "B", "C", or "D"
    points = Column(Integer, default=1)

    quiz = relationship("Quiz", back_populates="questions")


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Integer)
    percentage = Column(Float)
    time_spent = Column(Integer)  # seconds
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="results")
    quiz = relationship("Quiz", back_populates="results")



