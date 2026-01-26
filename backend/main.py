# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autentification.router import router as auth_router
from CRUD.results import router as results_router
from CRUD.questions import router as questions_router

app = FastAPI(title="Quiz System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволяємо всім
    allow_credentials=True,
    allow_methods=["*"],  # Дозволяємо всі методи
    allow_headers=["*"],  # Дозволяємо всі заголовки
)

app.include_router(auth_router)
app.include_router(results_router)
app.include_router(questions_router)

@app.get("/")
def root():
    return {"msg": "API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Quiz System API"}