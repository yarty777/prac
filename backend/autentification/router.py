from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from enum import Enum
from database import users_collection
import os
from pydantic import BaseModel, Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# ---------------- CONFIG ----------------
SECRET_KEY = os.getenv("SECRET_KEY", "DEV_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------- SECURITY ----------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------------- MODELS ----------------
class Role(str, Enum):
    teacher = "teacher"
    student = "student"

class UserCreate(BaseModel):
    email: str 
    password: str
    role: Role = Role.student

class LoginRequest(BaseModel):
    email: str 
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    email: str
    id: str  # Змінили з Optional[str] на str - завжди повертаємо ID

# PASSWORD UTILS (залишаємо без змін)
def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except Exception as e:
        logger.warning(f"Password verification failed: {e}")
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest() == hashed

# TOKEN UTILS 
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# CURRENT USER - ФІКСУЄМО ТУТ
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

        # ГАРАНТУЄМО, що повертаємо id з MongoDB _id
        return {
            "email": email, 
            "role": role, 
            "id": str(user.get("_id"))  # Завжди повертаємо id
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# RBAC (залишаємо без змін)
def require_role(role: Role):
    def checker(user=Depends(get_current_user)):
        if user["role"] != role.value:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker

# ROUTER 
router = APIRouter(prefix="/auth", tags=["Auth"])

# REGISTER - ФІКСУЄМО ТУТ
@router.post("/register", response_model=dict)
def register(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    
    new_user = {
        "email": user.email,
        "password": hashed_password,
        "role": user.role.value if isinstance(user.role, Role) else user.role
    }

    result = users_collection.insert_one(new_user)
    
    logger.info(f"User registered: {user.email}")
    
    # ГАРАНТУЄМО, що повертаємо id
    return {
        "message": "User created successfully",
        "id": str(result.inserted_id),  # Повертаємо як id
        "email": user.email,
        "role": user.role.value if isinstance(user.role, Role) else user.role
    }

# LOGIN - ФІКСУЄМО ТУТ
@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Ендпоінт для входу в систему.
    """
    user = users_collection.find_one({"email": login_data.email})
    
    if not user:
        logger.warning(f"Login failed: User {login_data.email} not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    logger.info(f"User found: {login_data.email}, checking password...")
    
    if not verify_password(login_data.password, user["password"]):
        logger.warning(f"Login failed: Invalid password for {login_data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # ГАРАНТУЄМО, що в токені є всі дані
    token = create_access_token({
        "sub": user["email"],
        "role": user["role"]
    })

    logger.info(f"Login successful: {login_data.email}")
    
    # ГАРАНТУЄМО, що повертаємо id
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        role=user["role"],
        email=user["email"],
        id=str(user.get("_id"))  # Завжди повертаємо id
    )

# FIX EXISTING USERS (залишаємо без змін)
@router.post("/fix-passwords")
def fix_existing_users():
    fixed_count = 0
    users = users_collection.find({})
    
    for user in users:
        current_password = user["password"]
        
        if len(current_password) < 30 or "$" not in current_password:
            new_hashed = hash_password(current_password)
            users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"password": new_hashed}}
            )
            fixed_count += 1
            logger.info(f"Fixed password for user: {user['email']}")
    
    return {
        "message": f"Fixed {fixed_count} user passwords",
        "fixed_count": fixed_count
    }


    # Кінець router.py - додай це:

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@router.get("/teacher-only")
async def teacher_only_endpoint(current_user: dict = Depends(get_current_user)):
    """Teacher-only endpoint"""
    if current_user.get("role") != "teacher":
        raise HTTPException(
            status_code=403,  # Просто 403, без status.HTTP_403_FORBIDDEN
            detail="Teacher access required"
        )
    return {"message": "Welcome, teacher!"}