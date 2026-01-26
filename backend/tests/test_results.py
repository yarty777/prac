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
    assert response.status_code == 200
    assert response.json()["msg"] == "Result saved"
