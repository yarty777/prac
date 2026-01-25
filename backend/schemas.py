from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str

class ResultCreate(BaseModel):
    score: int
    percentage: float
    time_spent: int

class ResultOut(ResultCreate):
    id: str
    user_id: str
    created_at: datetime
