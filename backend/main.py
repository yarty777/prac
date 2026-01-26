# main.py
from fastapi import FastAPI
from autentification.router import router as auth_router
from CRUD.results import router as results_router
from CRUD.questions import router as questions_router

app = FastAPI(title="Quiz System API")

app.include_router(auth_router)
app.include_router(results_router)
app.include_router(questions_router)

@app.get("/")
def root():
    return {"msg": "API is running"}
