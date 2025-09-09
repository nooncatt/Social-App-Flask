from http import HTTPStatus
from app.tests.factories import create_user_payload


def test_user_create(client):
    payload = create_user_payload()
    r1 = client.post("/users/create", json=payload)
    assert r1.status_code == HTTPStatus.CREATED
    r2 = client.post("/users/create", json=payload)
    assert r2.status_code == HTTPStatus.CONFLICT

    data = r1.get_json()
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]

    user_id = data["id"]
    r_get = client.get(f"/users/{user_id}")
    got = r_get.get_json()
    assert got["first_name"] == payload["first_name"]
    assert got["last_name"] == payload["last_name"]
    assert got["email"] == payload["email"]


def test_user_create_wrong_data(client):
    payload = create_user_payload()
    payload["email"] = "vasyagmail.com"
    response = client.post("/users/create", json=payload)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    payload = create_user_payload()
    response = client.post("/users/create", json=payload)
    assert response.status_code == HTTPStatus.CREATED

    user_id = response.get_json()["id"]
    deleted_user = client.delete(f"/users/{user_id}")
    assert deleted_user.status_code == HTTPStatus.OK
    assert deleted_user.get_json()["status"] == "deleted"
