def test_create_question(client):
    response = client.post(
        "/questions/",
        json={
            "quiz_id": "quiz1",
            "text": "2 + 2 = ?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "4",
            "points": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "2 + 2 = ?"


def test_get_questions_by_quiz(client):
    response = client.get("/questions/quiz/quiz1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
