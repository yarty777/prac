from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class QuizModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    topic: str
    difficulty: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuestionModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    quiz_id: str
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    points: int = 1
