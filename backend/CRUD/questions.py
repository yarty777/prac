from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from database import questions_collection
from models import QuestionModel


router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=QuestionModel)
def create_question(question: QuestionModel):
    doc = question.dict(by_alias=True, exclude={"id"})
    result = questions_collection.insert_one(doc)

    doc["_id"] = str(result.inserted_id)
    return doc

@router.get("/", response_model=list[QuestionModel])
def get_all_questions():
    questions = []

    for q in questions_collection.find():
        q["_id"] = str(q["_id"])
        questions.append(q)

    return questions

@router.get("/{question_id}", response_model=QuestionModel)
def get_question_by_id(question_id: str):
    question = questions_collection.find_one({"_id": ObjectId(question_id)})

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question["_id"] = str(question["_id"])
    return question

@router.get("/quiz/{quiz_id}", response_model=list[QuestionModel])
def get_questions_by_quiz_id(quiz_id: str):
    questions = []

    for q in questions_collection.find({"quiz_id": quiz_id}):
        q["_id"] = str(q["_id"])
        questions.append(q)

    return questions

@router.put("/{question_id}", response_model=QuestionModel)
def update_question(question_id: str, question: QuestionModel):
    update_data = question.dict(by_alias=True, exclude={"id"})

    result = questions_collection.update_one(
        {"_id": ObjectId(question_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    updated_question = questions_collection.find_one(
        {"_id": ObjectId(question_id)}
    )
    updated_question["_id"] = str(updated_question["_id"])

    return updated_question

@router.delete("/{question_id}")
def delete_question(question_id: str):
    result = questions_collection.delete_one(
        {"_id": ObjectId(question_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")

    return {"message": "Question deleted"}
