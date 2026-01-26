def test_create_result(client):
    response = client.post(
        "/results/?user_id=user1",
        json={
            "quiz_id": "quiz1",
            "score": 8,
            "percentage": 80.0,
            "time_spent": 120
        }
    )
    print("Response:", response.json())
    assert response.status_code == 200
    # Перевіряємо, що результат збережено (є _id в відповіді)
    assert "_id" in response.json()  # ← Заміни цей рядок