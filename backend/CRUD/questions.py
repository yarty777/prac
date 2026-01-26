from fastapi import APIRouter
from bson import ObjectId

from backend.database import questions_collection
from backend.schemas import QuestionCreate

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


def question_helper(q: dict) -> dict:
    return {
        "id": str(q["_id"]),
        "quiz_id": q["quiz_id"],
        "text": q["text"],
        "correct_answer": q["correct_answer"],
        "points": q["points"]
    }


@router.post("/")
def create_question(data: QuestionCreate):
    question = data.dict()
    result = questions_collection.insert_one(question)
    question["_id"] = result.inserted_id
    return question_helper(question)


@router.get("/quiz/{quiz_id}")
def get_questions_by_quiz(quiz_id: str):
    return [
        question_helper(q)
        for q in questions_collection.find({"quiz_id": quiz_id})
    ]
