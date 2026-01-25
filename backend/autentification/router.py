from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import users_collection
from autentification.hash import hash_password, verify_password
from autentification.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate): # type: ignore
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password)
    })

    return {"status": "registered"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form.username})

    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

