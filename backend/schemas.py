from pydantic import BaseModel
from typing import List, Optional
from database import datetime


# ---------- USER ----------
class UserBase(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    role: str

class ResultCreate(BaseModel):
    quiz_id: str
    score: int
    percentage: float
    time_spent: int


    class Config:
        from_attributes = True


# ---------- QUESTION ----------
class QuestionOut(BaseModel):
    id: int
    text: str
    answer: str

    class Config:
        from_attributes = True


# ---------- QUIZ ----------
class QuizOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    questions: List[QuestionOut] = []

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ResultOut(ResultCreate):
    id: str
    user_id: str
    completed_at: datetime

