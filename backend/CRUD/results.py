from fastapi import APIRouter, Depends, HTTPException
from database import results_collection
from schemas import ResultCreate
from datetime import datetime

router = APIRouter(prefix="/results", tags=["Results"])

@router.post("/")
def create_result(result: ResultCreate, user_id: str):
    data = result.dict()
    data["user_id"] = user_id
    data["created_at"] = datetime.utcnow()
    results_collection.insert_one(data)
    return {"status": "created"}

@router.get("/")
def get_results(user_id: str):
    return list(results_collection.find({"user_id": user_id}, {"_id": 0}))
