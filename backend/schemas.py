from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- USER ----------
class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: str
    username: str
    role: str


# ---------- QUIZ ----------
class QuizCreate(BaseModel):
    title: str
    topic: str
    author_id: str
    difficulty: int


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[int] = None


class QuizOut(BaseModel):
    id: str
    title: str
    topic: str
    author_id: str
    difficulty: int
    created_at: datetime


# ---------- QUESTION ----------
class QuestionCreate(BaseModel):
    quiz_id: str
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    points: int = 1


class QuestionOut(BaseModel):
    id: str
    quiz_id: str
    text: str
    correct_answer: str
    points: int


# ---------- RESULT ----------
class ResultCreate(BaseModel):
    quiz_id: str
    score: int
    percentage: float
    time_spent: int


class ResultOut(ResultCreate):
    id: str
    user_id: str
    completed_at: datetime
