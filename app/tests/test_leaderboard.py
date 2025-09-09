from http import HTTPStatus
import pytest
from uuid import uuid4
from app.tests.test_users import create_user_payload
from app.tests.test_posts import create_post_payload


@pytest.mark.parametrize(
    "leaderboard_type, sort_type", [("list", "asc"), ("graph", "desc")]
)
def test_get_users_sorted_leaderboard(client, leaderboard_type, sort_type):
    for _ in range(3):
        r = client.post("/users/create", json=create_user_payload())
        assert r.status_code == HTTPStatus.CREATED

    r = client.get(f"/users/leaderboard?type={leaderboard_type}&sort={sort_type}")

    if leaderboard_type == "list":
        assert r.status_code == HTTPStatus.OK
        data = r.get_json()
        assert isinstance(data, dict)
        assert "users" in data
        assert isinstance(data["users"], list)
        assert len(data["users"]) == 3

    elif leaderboard_type == "graph":
        assert r.status_code == HTTPStatus.OK
        data = r.get_json()
