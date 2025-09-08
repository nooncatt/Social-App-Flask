from http import HTTPStatus
from uuid import uuid4
from faker import Faker
import random
from app.tests.test_users import create_user_payload

fake = Faker("ru_RU")


def create_post_payload():
    return {
        "author_id": 0, # random.randint(0, 3), # number of created users
        "text": f"{fake.sentence()}",
    }

def test_create_post(client):
    # create user
    payload = create_user_payload()
    response = client.post("/users/create", json=payload)
    assert response.status_code == HTTPStatus.CREATED

    # create test post
    payload = create_post_payload()
    r = client.post("/posts/create", json=payload)
    assert r.status_code == HTTPStatus.CREATED

    data = r.get_json()
    assert data["author_id"] == payload["author_id"]
    assert data["text"] == payload["text"]

    post_id = data["id"]

    # get test post by id
    r_get = client.get(f"/posts/{post_id}")

    assert r_get.get_json()["author_id"] == payload["author_id"]
    assert r_get.get_json()["text"] == payload["text"]


def test_create_post_wrong_data(client):
    # create user
    payload = create_user_payload()
    response = client.post("/users/create", json=payload)
    assert response.status_code == HTTPStatus.CREATED

    payload = create_post_payload()
    payload["text"] = "" # wrong payload

    # create post
    r = client.post("/posts/create", json=payload)
    assert r.status_code == HTTPStatus.BAD_REQUEST


def get_user_posts(client):
    # create user with id 0
    payload = create_user_payload()
    response = client.post("/users/create", json=payload)
    assert response.status_code == HTTPStatus.CREATED

    # create some posts
    for _ in range(3):
        payload = create_post_payload()
        r = client.post("/posts/create", json=payload)
        assert r.status_code == HTTPStatus.CREATED

    user_id = response.get_json()["id"]
    r = client.get(f"/users/{user_id}/posts?sort=asc")
    user_posts_data = r.get_json()

    # todo: check убывание number of reactions ? но реакции еще не созданы ЧД?
    assert user_posts_data["text"] == payload["text"] # todo: check работает ли
    # assert user_posts_data["reactions"] =


'''
def test_delete_user(client):
    payload = create_user_payload()
    r = client.post("/users/create", json=payload)
    assert r.status_code == HTTPStatus.CREATED

    user_id = r.get_json()["id"]
    deleted_user = client.delete(f"/users/{user_id}")
    assert deleted_user.status_code == HTTPStatus.OK
    assert deleted_user.get_json()["status"] == "deleted"
'''




