from fastapi import APIRouter, Depends, HTTPException  # 👈 Додай HTTPException
from database import results_collection
from database import questions_collection
from schemas import ResultCreate
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/results", tags=["Results"])

@router.post("/")
def create_result(result: ResultCreate, user_id: str):
    doc = {
        "user_id": user_id,
        "quiz_id": result.quiz_id,
        "score": result.score,
        "percentage": result.percentage,
        "time_spent": result.time_spent,
        "completed_at": datetime.utcnow()
    }

    res = results_collection.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc

@router.get("/")
def get_results():
    results = []
    for r in results_collection.find():
        r["_id"] = str(r["_id"])
        results.append(r)
    return results

@router.get("/{user_id}") 
def get_results_by_user(user_id: str):
    """Отримати всі результати конкретного користувача"""
    results = []
    for r in results_collection.find({"user_id": user_id}):
        r["_id"] = str(r["_id"])
        results.append(r)
    
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this user")
    
    return results

@router.delete("/{item_id}")
def delete_result(item_id: str):
    result = results_collection.delete_one({"_id": ObjectId(item_id)})
    return {"deleted_count": result.deleted_count}

@router.get("/quiz/{quiz_id}")
def get_questions_by_quiz_id(quiz_id: str):
    questions = []

    for q in questions_collection.find({"quiz_id": quiz_id}):
        q["_id"] = str(q["_id"])
        questions.append(q)

    return questions