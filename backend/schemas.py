from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# -------------------- QUIZZES --------------------
class QuizCreate(BaseModel):
    title: str
    topic: str
    difficulty: int

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[int] = None

# -------------------- QUESTIONS --------------------
class QuestionCreate(BaseModel):
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    points: int = 1
