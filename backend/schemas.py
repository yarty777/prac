from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class UserBase(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    role: str
class UserCreate(BaseModel):
    username: str
    password: str
class ResultCreate(BaseModel):
    quiz_id: str
    score: int
    percentage: float
    time_spent: int


    class Config:
        from_attributes = True


class QuestionOut(BaseModel):
    id: int
    text: str
    answer: str

    class Config:
        from_attributes = True

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

