from fastapi import APIRouter, HTTPException
from bson import ObjectId

from database import questions_collection
from schemas import QuestionCreate, QuestionUpdate

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


def question_helper(q: dict) -> dict:
    return {
        "id": str(q["_id"]),
        "quiz_id": q["quiz_id"],
        "text": q["text"],
        "option_a": q["option_a"],
        "option_b": q["option_b"],
        "option_c": q["option_c"],
        "option_d": q["option_d"],
        "correct_answer": q["correct_answer"],
        "points": q.get("points", 1)  # Значення за замовчуванням
    }


@router.post("/")
def create_question(data: QuestionCreate):
    """Створити нове питання"""
    question = data.dict()
    result = questions_collection.insert_one(question)
    question["_id"] = result.inserted_id
    return question_helper(question)


@router.get("/")
def get_all_questions():
    """Отримати всі питання"""
    return [
        question_helper(q)
        for q in questions_collection.find()
    ]


@router.get("/{question_id}")
def get_question(question_id: str):
    """Отримати питання за ID"""
    question = questions_collection.find_one({"_id": ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question_helper(question)


@router.get("/quiz/{quiz_id}")
def get_questions_by_quiz(quiz_id: str):
    """Отримати всі питання для конкретного тесту"""
    return [
        question_helper(q)
        for q in questions_collection.find({"quiz_id": quiz_id})
    ]


@router.put("/{question_id}")
def update_question(question_id: str, data: QuestionUpdate):
    """Оновити питання"""
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    result = questions_collection.update_one(
        {"_id": ObjectId(question_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    
    updated_question = questions_collection.find_one({"_id": ObjectId(question_id)})
    return question_helper(updated_question)


@router.delete("/{question_id}")
def delete_question(question_id: str):
    """Видалити питання"""
    result = questions_collection.delete_one({"_id": ObjectId(question_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return {"message": "Question deleted successfully"}


@router.delete("/quiz/{quiz_id}")
def delete_questions_by_quiz(quiz_id: str):
    """Видалити всі питання для конкретного тесту"""
    result = questions_collection.delete_many({"quiz_id": quiz_id})
    
    return {
        "message": f"Deleted {result.deleted_count} questions for quiz {quiz_id}"
    }