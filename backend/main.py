# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autentification.router import router as auth_router
from CRUD.results import router as results_router
from CRUD.questions import router as questions_router
from CRUD.quizzes import router as quizzes_router

app = FastAPI(title="Quiz System API")

# Додайте CORS middleware ПЕРШИМ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Потім підключайте роутери
app.include_router(auth_router)
app.include_router(results_router)
app.include_router(questions_router)
app.include_router(quizzes_router)

@app.get("/")
def root():
    return {"msg": "API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Quiz System API"}