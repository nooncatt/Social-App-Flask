from app import POSTS
from app.tests.factories import (
    create_user_payload,
    create_post_payload,
    create_react_payload,
)
from http import HTTPStatus


def test_add_reaction(client):
    # create user
    user_resp = client.post("/users/create", json=create_user_payload())
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    # create test post
    r = client.post("/posts/create", json=create_post_payload(user_id))
    assert r.status_code == HTTPStatus.CREATED
    post_id = r.get_json()["id"]

    # create reaction
    react_payload = create_react_payload(user_id)
    reaction_post = client.post(f"/posts/{post_id}/reaction", json=react_payload)
    assert reaction_post.status_code == HTTPStatus.NO_CONTENT

    assert any(
        react_payload["reaction"] == r["reaction"] for r in POSTS[post_id].reactions
    )


def test_add_reaction_wrong_data(client):
    # create user
    user_resp = client.post("/users/create", json=create_user_payload())
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    # create test post
    r = client.post("/posts/create", json=create_post_payload(user_id))
    assert r.status_code == HTTPStatus.CREATED
    post_id = r.get_json()["id"]

    # create reaction
    react_payload = create_react_payload(user_id)
    react_payload["reaction"] = "lololo"
    reaction_post = client.post(f"/posts/{post_id}/reaction", json=react_payload)
    assert reaction_post.status_code == HTTPStatus.BAD_REQUEST


def test_add_reaction_change(client):
    # create user
    user_resp = client.post("/users/create", json=create_user_payload())
    assert user_resp.status_code == HTTPStatus.CREATED
    user_id = user_resp.get_json()["id"]

    # create test post
    r = client.post("/posts/create", json=create_post_payload(user_id))
    assert r.status_code == HTTPStatus.CREATED
    post_id = r.get_json()["id"]

    # create reaction
    react_payload1 = create_react_payload(user_id)
    reaction_post1 = client.post(f"/posts/{post_id}/reaction", json=react_payload1)
    assert reaction_post1.status_code == HTTPStatus.NO_CONTENT
    numb_of_react = len(POSTS[post_id].reactions)

    # same user new reaction
    react_payload2 = create_react_payload(user_id)
    reaction_post2 = client.post(f"/posts/{post_id}/reaction", json=react_payload2)
    assert reaction_post2.status_code == HTTPStatus.NO_CONTENT
    assert len(POSTS[post_id].reactions) == numb_of_react
    assert react_payload2["reaction"] == POSTS[post_id].reactions[-1]["reaction"]
