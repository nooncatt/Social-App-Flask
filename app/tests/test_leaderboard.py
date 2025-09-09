from http import HTTPStatus
import pytest
import os
from app.tests.test_users import create_user_payload


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

        # check that response have <img> in HTML
        html_content = r.get_data(as_text=True)
        assert "<img src=" in html_content

        # check that img file is in static catalog
        image_path = "app/static/leaderboard_graph.png"
        assert os.path.exists(
            image_path
        ), f"Expected image at {image_path}, but it does not exist"
