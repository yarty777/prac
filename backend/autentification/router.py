from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from enum import Enum
from database import users_collection
import os
from pydantic import BaseModel

# ---------------- CONFIG ----------------
SECRET_KEY = os.getenv("SECRET_KEY", "DEV_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------- SECURITY ----------------
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------------- ROLES ----------------
class Role(str, Enum):
    teacher = "teacher"
    student = "student"

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "student"

# ---------------- PASSWORD UTILS ----------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# ---------------- TOKEN UTILS ----------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------- CURRENT USER ----------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")

        if not email or not role:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {"email": email, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------------- RBAC ----------------
def require_role(role: Role):
    def checker(user=Depends(get_current_user)):
        if user["role"] != role.value:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker

# ---------------- ROUTER ----------------
router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------- REGISTER ----------------
@router.post("/register")
def register(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = {
        "email": user.email,
        "password": hash_password(user.password),
        "role": user.role
    }

    users_collection.insert_one(new_user)
    return {"message": "User created"}

# ---------------- LOGIN ----------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["email"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }

# ---------------- PROTECTED ROUTES ----------------
@router.get("/teacher-only")
def teacher_only(user=Depends(require_role(Role.teacher))):
    return {"msg": "Hello teacher"}

@router.get("/student-only")
def student_only(user=Depends(require_role(Role.student))):
    return {"msg": "Hello student"}
