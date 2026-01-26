import pytest

# Фікстури з conftest.py будуть автоматично доступні

@pytest.fixture(autouse=True)
def clear_users():
    """Очищаємо користувачів перед кожним тестом"""
    import database
    database.users_collection.delete_many({})
    yield
    database.users_collection.delete_many({})


# tests/integration/test_auth_integration.py
import pytest
import time

@pytest.mark.asyncio
async def test_register_user(async_client):
    """Тест реєстрації з унікальним email"""
    # Додаємо timestamp щоб email був унікальним
    timestamp = int(time.time())
    email = f"student_{timestamp}@test.com"
    
    response = await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "123456",
            "role": "student"
        }
    )
    
    print(f"📧 Used email: {email}")
    print(f"📨 Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_login_user(async_client):
    # Спочатку реєструємо
    await async_client.post(
        "/auth/register",
        json={
            "email": "login@test.com",
            "password": "123456",
            "role": "student"
        }
    )

    # Потім логінимось
    response = await async_client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_me(async_client):
    # Реєстрація
    await async_client.post(
        "/auth/register",
        json={
            "email": "me@test.com",
            "password": "123456",
            "role": "student"
        }
    )

    # Логін
    login = await async_client.post(
        "/auth/login",
        json={
            "email": "me@test.com",
            "password": "123456"
        }
    )
    token = login.json()["access_token"]

    # Отримання даних про себе
    me = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert me.status_code == 200
    assert me.json()["email"] == "me@test.com"


@pytest.mark.asyncio
async def test_teacher_only_forbidden(async_client):
    # Реєстрація студента
    await async_client.post(
        "/auth/register",
        json={
            "email": "student2@test.com",
            "password": "123456",
            "role": "student"
        }
    )

    # Логін студента
    login = await async_client.post(
        "/auth/login",
        json={
            "email": "student2@test.com",
            "password": "123456"
        }
    )
    token = login.json()["access_token"]

    # Спроба доступу до teacher-only endpoint
    response = await async_client.get(
        "/auth/teacher-only",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403