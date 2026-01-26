def test_create_quiz(client):
    response = client.post(
        "/quizzes/",
        json={
            "title": "Python Test",
            "topic": "Python",
            "author_id": "user1",
            "difficulty": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python Test"
    assert data["topic"] == "Python"


def test_get_quizzes(client):
    response = client.get("/quizzes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
