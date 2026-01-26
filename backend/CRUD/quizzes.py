from fastapi import APIRouter, HTTPException
from bson import ObjectId

from database import quizzes_collection
from schemas import QuizCreate, QuizUpdate

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"]
)


def quiz_helper(quiz: dict) -> dict:
    return {
        "id": str(quiz["_id"]),
        "title": quiz["title"],
        "topic": quiz["topic"],
        "author_id": quiz["author_id"],
        "difficulty": quiz["difficulty"],
        "created_at": quiz.get("created_at", datetime.utcnow())
    }


@router.get("/")
def get_quizzes():
    return [quiz_helper(q) for q in quizzes_collection.find()]


@router.get("/{quiz_id}")
def get_quiz(quiz_id: str):
    quiz = quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz_helper(quiz)


@router.post("/")
def create_quiz(data: QuizCreate):
    quiz = data.dict()
    result = quizzes_collection.insert_one(quiz)
    quiz["_id"] = result.inserted_id
    return quiz_helper(quiz)


@router.put("/{quiz_id}")
def update_quiz(quiz_id: str, data: QuizUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    result = quizzes_collection.update_one(
        {"_id": ObjectId(quiz_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
    return quiz_helper(quiz)


@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: str):
    result = quizzes_collection.delete_one({"_id": ObjectId(quiz_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {"msg": "Quiz deleted"}
