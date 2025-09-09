from http import HTTPStatus
from uuid import uuid4
from app.tests.test_users import create_user_payload
from app.tests.test_posts import create_post_payload


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
