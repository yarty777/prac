import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app

class FakeCollection:
    def __init__(self):
        self.data = []

    def insert_one(self, item):
        item["_id"] = "fake_id"
        self.data.append(item)
        return type("obj", (), {"inserted_id": "fake_id"})

    def find(self, query=None):
        return self.data

    def find_one(self, query):
        for item in self.data:
            return item
        return None

    def update_one(self, query, update):
        if self.data:
            self.data[0].update(update["$set"])
            return type("obj", (), {"matched_count": 1})
        return type("obj", (), {"matched_count": 0})

    def delete_one(self, query):
        if self.data:
            self.data.pop()
            return type("obj", (), {"deleted_count": 1})
        return type("obj", (), {"deleted_count": 0})


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    from backend import database

    database.quizzes_collection = FakeCollection()
    database.questions_collection = FakeCollection()
    database.results_collection = FakeCollection()


@pytest.fixture
def client():
    return TestClient(app)
