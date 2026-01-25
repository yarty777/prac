from fastapi import APIRouter, Depends
from database import results_collection
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

@router.delete("/{item_id}")
def delete_result(item_id: str):
    result = results_collection.delete_one({"_id": ObjectId(item_id)})
    return {"deleted_count": result.deleted_count}

    
