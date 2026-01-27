import pytest

@pytest.fixture(autouse=True)
def clear_db():
    """Очищаємо всю базу перед кожним тестом"""
    import database
    database.users_collection.delete_many({})
    database.questions_collection.delete_many({})
    database.results_collection.delete_many({})
    database.quizzes_collection.delete_many({})
    yield
    database.users_collection.delete_many({})
    database.questions_collection.delete_many({})
    database.results_collection.delete_many({})
    database.quizzes_collection.delete_many({})


@pytest.mark.asyncio
async def test_full_system(async_client):
    # 1) Register teacher
    teacher_res = await async_client.post(
        "/auth/register",
        json={
            "email": "teacher@test.com",
            "password": "123456",
            "role": "teacher"
        }
    )
    
    print(f"🔍 Teacher register status: {teacher_res.status_code}")
    print(f"🔍 Teacher register body: {teacher_res.json()}")  # ← Додай цей рядок
    
    assert teacher_res.status_code == 200

    # --------------------
    # 2) Login teacher
    # --------------------
    login_teacher = await async_client.post(
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
    question_res = await async_client.post(
        "/questions/",
        json={
            "quiz_id": "quiz_1",
            "text": "What is 2+2?",
            "option_a": "1",
            "option_b": "2",
            "option_c": "4",
            "option_d": "5",
            "correct_answer": "C",  # Має бути одна велика буква
            "points": 1
        }
    )
    assert question_res.status_code == 200
    question_data = question_res.json()
    # Спробуй різні варіанти ключів
    question_id = question_data.get("_id") or question_data.get("id") or question_data.get("question_id")
    print(f"📌 Question ID: {question_id}")
    # --------------------
    # 4) Get all questions
    # --------------------
    questions = await async_client.get("/questions/")
    assert questions.status_code == 200
    assert len(questions.json()) == 1

    # --------------------
    # 5) Register student
    # --------------------
    student_res = await async_client.post(
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
    login_student = await async_client.post(
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
    result_res = await async_client.post(
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
    teacher_only = await async_client.get(
        "/auth/teacher-only",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert teacher_only.status_code == 403

    # --------------------
    # 9) Check student can access their results
    # --------------------
    results = await async_client.get(
        "/results/student_id"
    )
    assert results.status_code == 200
    assert len(results.json()) == 1