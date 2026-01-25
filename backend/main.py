from fastapi import FastAPI
from autentification.router import router as auth_router
from CRUD.results import router as results_router

app = FastAPI(title="Quiz System API")

app.include_router(auth_router)
app.include_router(results_router)

