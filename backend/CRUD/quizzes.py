# CRUD/quizzes.py
from fastapi import APIRouter, HTTPException
from database import quizzes_collection
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

class QuizCreate(BaseModel):
    title: str
    topic: str
    difficulty: int = 1

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[int] = None

@router.post("/")
def create_quiz(quiz: QuizCreate):
    """Створити новий тест (доступно всім без автентифікації)"""
    
    quiz_data = {
        "title": quiz.title,
        "topic": quiz.topic,
        "difficulty": quiz.difficulty,
        "created_at": datetime.utcnow()
    }
    
    result = quizzes_collection.insert_one(quiz_data)
    quiz_data["_id"] = str(result.inserted_id)
    return quiz_data

@router.get("/")
def get_quizzes():
    """Отримати всі тести"""
    quizzes = []
    for quiz in quizzes_collection.find():
        quiz["_id"] = str(quiz["_id"])
        quizzes.append(quiz)
    return quizzes

@router.get("/my")
def get_my_quizzes():
    """Отримати мої тести (заглушка, бо немає автентифікації)"""
    return {"message": "No authentication - showing all quizzes instead", "quizzes": []}

@router.put("/{quiz_id}")
def update_quiz(quiz_id: str, quiz_update: QuizUpdate):
    """Оновити тест (доступно всім без автентифікації)"""
    
    # Перевіряємо, чи існує квіз
    try:
        object_id = ObjectId(quiz_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid quiz ID")
    
    quiz = quizzes_collection.find_one({"_id": object_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Готуємо оновлення
    update_data = {}
    if quiz_update.title is not None:
        update_data["title"] = quiz_update.title
    if quiz_update.topic is not None:
        update_data["topic"] = quiz_update.topic
    if quiz_update.difficulty is not None:
        update_data["difficulty"] = quiz_update.difficulty
    
    # Додаємо час оновлення
    update_data["updated_at"] = datetime.utcnow()
    
    # Оновлюємо
    quizzes_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )
    
    # Отримуємо оновлений квіз
    updated_quiz = quizzes_collection.find_one({"_id": object_id})
    updated_quiz["_id"] = str(updated_quiz["_id"])
    return updated_quiz

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: str):
    """Видалити тест (доступно всім без автентифікації)"""
    
    # Перевіряємо, чи існує квіз
    try:
        object_id = ObjectId(quiz_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid quiz ID")
    
    quiz = quizzes_collection.find_one({"_id": object_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Видаляємо
    result = quizzes_collection.delete_one({"_id": object_id})
    
    return {"message": "Quiz deleted successfully", "quiz_id": quiz_id}