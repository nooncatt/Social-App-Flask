import requests
from http import HTTPStatus
from uuid import uuid4

def create_user_payload():
    return {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pypkin" + str(uuid4()),
        "email": f"vasya{uuid4()}@gmail.com",
    }


def test_get_users_sorted_leaderboard(client):
    for _ in range(3):
        r = client.post("/users/create", json=create_user_payload())
        assert r.status_code == HTTPStatus.CREATED

    r = client.get("/users/leaderboard?type=list&sort=asc")
    assert r.status_code == HTTPStatus.OK
    data = r.get_json()
    assert isinstance(data, dict)
    assert "users" in data
    assert isinstance(data["users"], list)
    assert len(data["users"]) == 3





