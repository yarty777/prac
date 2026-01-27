# tests/conftest.py     python -m pytest tests/ -v      
import sys
import os
import pytest

# Додаємо поточну директорію tests/ до шляху
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Тепер імпортуємо з tests/
try:
    from unit_database import setup_unit_test_database
except ImportError:
    # Спробуємо інший шлях
    from .unit_database import setup_unit_test_database

# Налаштовуємо фейкову базу
setup_unit_test_database()

# Додаємо шлях до кореня проекту для імпорту app
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Тепер імпортуємо app (він буде використовувати фейкову базу)
from main import app

@pytest.fixture
def client():
    """Клієнт для юніт-тестів"""
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_unit_db():
    """Очищаємо фейкову базу після кожного юніт-тесту"""
    import database
    yield
    # Очищаємо всі колекції
    for attr in ['users_collection', 'quizzes_collection', 
                 'questions_collection', 'results_collection']:
        if hasattr(database, attr):
            collection = getattr(database, attr)
            if hasattr(collection, 'delete_many'):
                collection.delete_many({})
    print("🧹 Unit test DB cleaned")