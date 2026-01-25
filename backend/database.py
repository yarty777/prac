from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if not ENV_PATH.exists():
    raise RuntimeError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH)

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise RuntimeError("MONGO_URL is not set in .env")

client = MongoClient(MONGO_URL)
db = client["System_Test"]

users_collection = db["users"]
results_collection = db["results"]

print("MongoDB connected")
