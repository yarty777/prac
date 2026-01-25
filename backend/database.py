from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL is not set")

client = MongoClient(MONGO_URL)
db = client["System_Test"]

users_collection = db["users"]
quizzes_collection = db["quizzes"]
questions_collection = db["questions"]
results_collection = db["results"]

print("MongoDB connected")

