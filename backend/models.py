from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: Optional[str] = None
    role: str = "user"

class QuizModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    topic: str
    author_id: str
    difficulty: int
    created_at: datetime = datetime.utcnow()

class QuestionModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    quiz_id: str
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    points: int = 1

class ResultModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    quiz_id: str
    score: int
    percentage: float
    time_spent: int
    completed_at: datetime = datetime.utcnow()

