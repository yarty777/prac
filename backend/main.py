from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from autentification.router import router as auth_router
from CRUD.results import router as results_router
from CRUD.questions import router as questions_router
from CRUD.quizzes import router as quizzes_router
=======

from backend.autentification.router import router as auth_router
from backend.CRUD.quizzes import router as quizzes_router
from backend.CRUD.questions import router as questions_router
from backend.CRUD.results import router as results_router
>>>>>>> 71f2280 (test)

app = FastAPI(title="Quiz System API")

# Додайте CORS middleware ПЕРШИМ
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
=======
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
>>>>>>> 71f2280 (test)
)

# Потім підключайте роутери
app.include_router(auth_router)
app.include_router(quizzes_router)
app.include_router(questions_router)
<<<<<<< HEAD
app.include_router(quizzes_router)
=======
app.include_router(results_router)

>>>>>>> 71f2280 (test)

@app.get("/")
def root():
    return {"msg": "API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
