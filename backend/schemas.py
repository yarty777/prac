from pydantic import BaseModel
from typing import List, Optional


# ---------- USER ----------
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int

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
