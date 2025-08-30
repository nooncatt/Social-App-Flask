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
                "reactions": [r["reaction"] for r in post.reactions],
            }
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
                "reactions": [r["reaction"] for r in post.reactions],
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


@app.get("/users/<int:user_id>/posts")
def get_user_posts(user_id):

    sort_param = request.args.get("sort")  # asc - по возрастанию, desc - по убыванию

    if sort_param not in {"asc", "desc"}:
        return Response("Invalid sort (use asc/desc)", HTTPStatus.BAD_REQUEST)

    reverse = sort_param != "asc"

    if not models.User.is_valid_id(user_id):
        return Response("User with this id doesn't exist", HTTPStatus.NOT_FOUND)

    user = USERS[user_id]

    posts = [POSTS[p_id] for p_id in user.posts if models.Post.is_valid_post_id(p_id)]

    posts.sort(key=lambda p: p.reactions_counter(), reverse=reverse)

    payload = {
        "posts": [
            {
                "id": p.id,
                "author_id": p.author_id,
                "text": p.text,
                "reactions": [r["reaction"] for r in p.reactions],
            }
            for p in posts
        ]
    }

    response = Response(
        json.dumps(payload),
        mimetype="application/json",
        status=HTTPStatus.OK,
    )

    return response


@app.get("/users/leaderboard")
def get_users_sorted_leaderboard():  # asc - по возрастанию, desc - по убыванию

    data_type = request.args.get("type")  # "list"
    sort_param = request.args.get("sort")  # "asc/desc"

    if len(USERS) == 0:
        return Response("No users on platform", HTTPStatus.NOT_FOUND)

    if data_type != "list":
        return Response("Invalid data type", HTTPStatus.BAD_REQUEST)

    if sort_param not in {"asc", "desc"}:
        return Response("Invalid sort (use asc/desc)", HTTPStatus.BAD_REQUEST)

    reverse = sort_param != "asc"

    USERS.sort(key=lambda u: u.total_reactions, reverse=reverse)

    payload = {
        "users": [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "total_reactions": u.total_reactions,
            }
            for u in USERS
        ]
    }

    response = Response(
        json.dumps(payload),
        mimetype="application/json",
        status=HTTPStatus.OK,
    )

    return response


@app.get("/users/leaderboard")
def get_leaderboard():
    data_type = request.args.get("type")

    if data_type != "graph":
        return Response("Invalid data type", HTTPStatus.BAD_REQUEST)


# <img src="path_to_graph">
