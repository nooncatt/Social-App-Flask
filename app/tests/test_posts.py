from http import HTTPStatus
from app.tests.factories import create_user_payload, create_post_payload
import pytest


def test_create_post(client):
    # create user
    user_payload = create_user_payload()
    user_resp = client.post("/users/create", json=user_payload)
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    # create test post
    post_payload = create_post_payload(user_id)
    r = client.post("/posts/create", json=post_payload)
    assert r.status_code == HTTPStatus.CREATED
    data = r.get_json()
    assert data["author_id"] == post_payload["author_id"]
    assert data["text"] == post_payload["text"]
    assert r.get_json()["reactions"] == []

    post_id = data["id"]

    # get test post by id
    r_get = client.get(f"/posts/{post_id}")

    assert r_get.get_json()["author_id"] == post_payload["author_id"]
    assert r_get.get_json()["text"] == post_payload["text"]


def test_create_post_wrong_data(client):
    # create user
    user_payload = create_user_payload()
    user_resp = client.post("/users/create", json=user_payload)
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    post_payload = create_post_payload(user_id)
    post_payload["text"] = ""  # wrong payload

    # create post
    r = client.post("/posts/create", json=post_payload)
    assert r.status_code == HTTPStatus.BAD_REQUEST


def test_create_post_author_not_found(client):
    payload = create_post_payload(999)
    r = client.post("/posts/create", json=payload)
    assert r.status_code == HTTPStatus.NOT_FOUND


def test_get_post_invalid_id(client):
    r = client.get("/posts/9999")
    assert r.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_posts(client):
    # create user
    user_payload = create_user_payload()
    user_resp = client.post("/users/create", json=user_payload)
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    # create some posts
    for _ in range(3):
        post_payload = create_post_payload(user_id)
        r = client.post("/posts/create", json=post_payload)
        assert r.status_code == HTTPStatus.CREATED

    r = client.get(f"/users/{user_id}/posts", query_string={"sort": "asc"})
    user_posts_data = r.get_json()
    assert isinstance(user_posts_data, dict)
    assert "posts" in user_posts_data
    posts = user_posts_data["posts"]
    assert isinstance(posts, list)
    assert len(posts) == 3
    assert all(item["author_id"] == user_id for item in posts)


@pytest.mark.parametrize("order, reverse", [("asc", False), ("desc", True)])
def test_get_user_posts_sorted_by_reactions(client, order, reverse):
    # create users
    user_id = client.post("/users/create", json=create_user_payload()).get_json()["id"]
    user_id1 = client.post("/users/create", json=create_user_payload()).get_json()["id"]
    user_id2 = client.post("/users/create", json=create_user_payload()).get_json()["id"]

    # create some posts
    post_id1 = client.post(
        "/posts/create", json=create_post_payload(user_id)
    ).get_json()["id"]
    post_id2 = client.post(
        "/posts/create", json=create_post_payload(user_id)
    ).get_json()["id"]
    post_id3 = client.post(
        "/posts/create", json=create_post_payload(user_id)
    ).get_json()["id"]

    client.post(
        f"/posts/{post_id1}/reaction", json={"user_id": user_id1, "reaction": "wow"}
    )
    client.post(
        f"/posts/{post_id1}/reaction", json={"user_id": user_id1, "reaction": "wow"}
    )
    client.post(
        f"/posts/{post_id1}/reaction", json={"user_id": user_id2, "reaction": "wow"}
    )

    r = client.get(f"/users/{user_id}/posts", query_string={"sort": order})
    assert r.status_code == HTTPStatus.OK
    posts = r.get_json()["posts"]
    counts = [len(p["reactions"]) for p in posts]
    assert counts == sorted(counts, reverse=reverse)


def test_delete_post(client):
    # create user
    user_payload = create_user_payload()
    user_resp = client.post("/users/create", json=user_payload)
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    # create test post
    post_payload = create_post_payload(user_id)
    r_post = client.post("/posts/create", json=post_payload)
    assert r_post.status_code == HTTPStatus.CREATED

    post_id = r_post.get_json()["id"]

    r_delete = client.delete(f"/posts/{post_id}")
    assert r_delete.status_code == HTTPStatus.OK

    assert r_delete.get_json()["id"] == post_id
    assert r_delete.get_json()["author_id"] == post_payload["author_id"]
    assert r_delete.get_json()["text"] == post_payload["text"]
    assert r_delete.get_json()["status"] == "deleted"
