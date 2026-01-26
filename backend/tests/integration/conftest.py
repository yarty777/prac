# tests/integration/conftest.py
import sys
import os
import pytest

# Додаємо шляхи
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# 1. Підміняємо базу даних на фейкову ДО будь-яких імпортів
from integration_database import setup_integration_database
integration_db = setup_integration_database()

# 2. Тепер імпортуємо app (він буде використовувати фейкову базу)
from main import app

@pytest.fixture
async def async_client():
    """Асинхронний клієнт для тестування"""
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup_integration_db():
    """
    Очищаємо фейкову базу перед кожним тестом.
    Автоматично викликається для всіх тестів в integration/.
    """
    import database
    
    # Очищаємо всі колекції
    collections = ['users', 'quizzes', 'questions', 'results']
    for col_name in collections:
        collection = getattr(database, f"{col_name}_collection", None)
        if collection and hasattr(collection, 'delete_many'):
            collection.delete_many({})
    
    print("🧹 Integration DB cleaned before test")
    yield
    
    # Очищаємо після тесту
    for col_name in collections:
        collection = getattr(database, f"{col_name}_collection", None)
        if collection and hasattr(collection, 'delete_many'):
            collection.delete_many({})
    print("🧹 Integration DB cleaned after test")