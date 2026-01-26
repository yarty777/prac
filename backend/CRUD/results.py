from fastapi import APIRouter
from backend.database import results_collection
from backend.schemas import ResultCreate
from datetime import datetime

router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


@router.post("/")
def create_result(user_id: str, data: ResultCreate):
    result = data.dict()
    result["user_id"] = user_id
    result["completed_at"] = datetime.utcnow()

    results_collection.insert_one(result)
    return {"msg": "Result saved"}
