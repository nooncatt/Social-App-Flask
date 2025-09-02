from .. import app, models, USERS, POSTS
from flask import request, Response
from http import HTTPStatus
import json


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

    # сортируем временную выборку постов - поиск по id не ломается
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
