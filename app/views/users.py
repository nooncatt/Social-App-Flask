from .. import app, models, USERS
from flask import request, Response
from http import HTTPStatus
import json


@app.post("/users/create")
def create_user():
    data = request.get_json()

    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    user_id = len(USERS)

    if not models.User.check_email_validity(email):
        return Response("This email doesn't exist", HTTPStatus.NOT_FOUND)

    for curr_user in USERS:
        if curr_user.email.lower() == email.lower():
            return Response("User with this email already exists", HTTPStatus.CONFLICT)

    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)

    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )

    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response("User with this id doesn't exist", HTTPStatus.NOT_FOUND)

    user = USERS[user_id]

    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response("User with this id doesn't exist", HTTPStatus.NOT_FOUND)


    user = USERS[user_id]
    user.status = "deleted"

    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
                "status": user.status,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
