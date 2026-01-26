import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from database import users_collection


@pytest.fixture(autouse=True)
def clear_users():
    users_collection.delete_many({})
    yield
    users_collection.delete_many({})


@pytest.mark.asyncio
async def test_register_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/auth/register",
            json={
                "email": "student@test.com",
                "password": "123456",
                "role": "student"
            }
        )

    assert response.status_code == 200
    assert response.json()["email"] == "student@test.com"


@pytest.mark.asyncio
async def test_login_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={
                "email": "login@test.com",
                "password": "123456",
                "role": "student"
            }
        )

        response = await client.post(
            "/auth/login",
            json={
                "email": "login@test.com",
                "password": "123456"
            }
        )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_me():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={
                "email": "me@test.com",
                "password": "123456",
                "role": "student"
            }
        )

        login = await client.post(
            "/auth/login",
            json={
                "email": "me@test.com",
                "password": "123456"
            }
        )

        token = login.json()["access_token"]

        me = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert me.status_code == 200
    assert me.json()["email"] == "me@test.com"


@pytest.mark.asyncio
async def test_teacher_only_forbidden():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={
                "email": "student2@test.com",
                "password": "123456",
                "role": "student"
            }
        )

        login = await client.post(
            "/auth/login",
            json={
                "email": "student2@test.com",
                "password": "123456"
            }
        )

        token = login.json()["access_token"]

        response = await client.get(
            "/auth/teacher-only",
            headers={"Authorization": f"Bearer {token}"}
        )

    assert response.status_code == 403
