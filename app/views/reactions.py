from .. import app, models, USERS, POSTS
from flask import request, Response
from http import HTTPStatus


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
