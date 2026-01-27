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

     # --------------------
    # 10) Get question by ID
    # --------------------
    get_one = await async_client.get(f"/questions/{question_id}")
    assert get_one.status_code == 200
    assert get_one.json()["text"] == "What is 2+2?"

    # --------------------
    # 11) Get questions by quiz_id
    # --------------------
    quiz_questions = await async_client.get("/questions/quiz/quiz_1")
    assert quiz_questions.status_code == 200
    assert len(quiz_questions.json()) == 1

    # --------------------
    # 12) Update question
    # --------------------
    update_res = await async_client.put(
        f"/questions/{question_id}",
        json={
            "text": "What is 3+3?",
            "correct_answer": "C",
            "points": 2
        }
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["text"] == "What is 3+3?"
    assert updated["points"] == 2

    # --------------------
    # 13) Check updated question
    # --------------------
    check_update = await async_client.get(f"/questions/{question_id}")
    assert check_update.status_code == 200
    assert check_update.json()["text"] == "What is 3+3?"

    # --------------------
    # 14) Delete question by ID
    # --------------------
    delete_res = await async_client.delete(f"/questions/{question_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Question deleted successfully"

    # --------------------
    # 15) Ensure question is deleted
    # --------------------
    not_found = await async_client.get(f"/questions/{question_id}")
    assert not_found.status_code == 404

    # --------------------
    # 16) Create multiple questions for quiz
    # --------------------
    for i in range(3):
        res = await async_client.post(
            "/questions/",
            json={
                "quiz_id": "quiz_bulk",
                "text": f"Question {i}",
                "option_a": "A",
                "option_b": "B",
                "option_c": "C",
                "option_d": "D",
                "correct_answer": "A",
                "points": 1
            }
        )
        assert res.status_code == 200

    # --------------------
    # 17) Delete all questions by quiz_id
    # --------------------
    delete_bulk = await async_client.delete("/questions/quiz/quiz_bulk")
    assert delete_bulk.status_code == 200
    assert "Deleted 3 questions" in delete_bulk.json()["message"]

    # --------------------
    # 18) Ensure quiz questions are gone
    # --------------------
    check_bulk = await async_client.get("/questions/quiz/quiz_bulk")
    assert check_bulk.status_code == 200
    assert len(check_bulk.json()) == 0