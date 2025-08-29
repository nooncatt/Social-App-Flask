from . import app, models, USERS, POSTS
from flask import request, Response
from http import HTTPStatus
import json


@app.route("/")
def index():
    return "<h1>Hello world</h1>"


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

    user = USERS[user_id]  # if we don't delete users

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


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    author_id = data["author_id"]
    text = data["text"]
    post_id = len(POSTS)

    if not models.User.is_valid_author_id(author_id):
        return Response("Author with this id doesn't exist", HTTPStatus.NOT_FOUND)

    if len(text) == 0:
        return Response("You need to enter some text", HTTPStatus.BAD_REQUEST)

    post = models.Post(post_id, author_id, text)
    POSTS.append(post)
    USERS[author_id].posts.append(post_id)

    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,  # todo: check how it looks
            }  # "reactions": [r["reaction"] for r in post.reactions]
        ),
        mimetype="application/json",
        status=HTTPStatus.CREATED,
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if not models.Post.is_valid_post_id(post_id):
        return Response("Invalid post id", HTTPStatus.BAD_REQUEST)
    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        mimetype="application/json",
        status=HTTPStatus.OK,
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def add_reaction(post_id):

    if not models.Post.is_valid_post_id(post_id):
        return Response("Invalid post id", HTTPStatus.BAD_REQUEST)

    data = request.get_json()
    user_id = data["user_id"]
    reaction = data["reaction"]

    if not models.Post.is_valid_reaction(reaction):
        return Response("Invalid reaction", status=HTTPStatus.BAD_REQUEST)

    if not models.User.is_valid_id(user_id):
        return Response("User with this id doesn't exist", HTTPStatus.NOT_FOUND)

    post = POSTS[post_id]
    author = USERS[post.author_id]

    # check that 1 user can have only 1 reaction
    result = post.add_or_update_reaction(user_id, reaction)
    if result == "new":
        author.change_total_reactions(1)

    return Response(status=HTTPStatus.NO_CONTENT)
