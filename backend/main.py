from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from database import SessionLocal, engine
from models import Base, Quiz
from schemas import QuizOut, QuizCreate, QuizUpdate

app = FastAPI(title="Quiz System API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------- DB dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- ROOT ----------
@app.get("/")
def root():
    return {"message": "FastAPI is working"}


# ---------- QUIZZES ----------

@app.get("/quizzes", response_model=List[QuizOut])
def get_quizzes(db: Session = Depends(get_db)): # type: ignore
    return db.query(Quiz).all()


@app.get("/quizzes/{id}", response_model=QuizOut)
def get_quiz(id: int, db: Session = Depends(get_db)): # type: ignore
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@app.post("/quizzes", response_model=QuizOut, status_code=201)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)): # type: ignore
    new_quiz = Quiz(
        title=quiz.title,
        description=quiz.description
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@app.put("/quizzes/{id}", response_model=QuizOut)
def update_quiz(id: int, quiz_data: QuizUpdate, db: Session = Depends(get_db)): # type: ignore
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz_data.title is not None:
        quiz.title = quiz_data.title
    if quiz_data.description is not None:
        quiz.description = quiz_data.description

    db.commit()
    db.refresh(quiz)
    return quiz


@app.delete("/quizzes/{id}", status_code=204)
def delete_quiz(id: int, db: Session = Depends(get_db)): # type: ignore
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(quiz)
    db.commit()
