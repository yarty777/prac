import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from database import users_collection, questions_collection, results_collection


@pytest.fixture(autouse=True)
def clear_db():
    users_collection.delete_many({})
    questions_collection.delete_many({})
    results_collection.delete_many({})
    yield
    users_collection.delete_many({})
    questions_collection.delete_many({})
    results_collection.delete_many({})


@pytest.mark.asyncio
async def test_full_system():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        # --------------------
        # 1) Register teacher
        # --------------------
        teacher_res = await client.post(
            "/auth/register",
            json={
                "email": "teacher@test.com",
                "password": "123456",
                "role": "teacher"
            }
        )
        assert teacher_res.status_code == 200

        # --------------------
        # 2) Login teacher
        # --------------------
        login_teacher = await client.post(
            "/auth/login",
            json={
                "email": "teacher@test.com",
                "password": "123456"
            }
        )
        teacher_token = login_teacher.json()["access_token"]

        # --------------------
        # 3) Create question as teacher
        # --------------------
        question_res = await client.post(
            "/questions/",
            json={
                "quiz_id": "quiz_1",
                "text": "What is 2+2?",
                "option_a": "1",
                "option_b": "2",
                "option_c": "4",
                "option_d": "5",
                "correct_answer": "c",
                "points": 1
            }
        )
        assert question_res.status_code == 200
        question_id = question_res.json()["_id"]

        # --------------------
        # 4) Get all questions
        # --------------------
        questions = await client.get("/questions/")
        assert questions.status_code == 200
        assert len(questions.json()) == 1

        # --------------------
        # 5) Register student
        # --------------------
        student_res = await client.post(
            "/auth/register",
            json={
                "email": "student@test.com",
                "password": "123456",
                "role": "student"
            }
        )
        assert student_res.status_code == 200

        # --------------------
        # 6) Login student
        # --------------------
        login_student = await client.post(
            "/auth/login",
            json={
                "email": "student@test.com",
                "password": "123456"
            }
        )
        student_token = login_student.json()["access_token"]

        # --------------------
        # 7) Create result as student
        # --------------------
        result_res = await client.post(
            "/results/?user_id=student_id",
            json={
                "quiz_id": "quiz_1",
                "score": 1,
                "percentage": 100.0,
                "time_spent": 60
            }
        )
        assert result_res.status_code == 200

        # --------------------
        # 8) Check teacher-only endpoint
        # --------------------
        teacher_only = await client.get(
            "/auth/teacher-only",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert teacher_only.status_code == 403
