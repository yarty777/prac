from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

Base = declarative_base()
