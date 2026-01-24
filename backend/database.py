from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
# Підключення до MongoDB
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is not set in .env")

client = MongoClient(MONGO_URL)
db = client["System_Test"]
