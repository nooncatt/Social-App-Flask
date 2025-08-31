from .. import app, USERS
from flask import request, Response
from http import HTTPStatus
import json


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


# @app.get("/users/leaderboard")
# def get_leaderboard():
#     data_type = request.args.get("type")
#
#     if data_type != "graph":
#         return Response("Invalid data type", HTTPStatus.BAD_REQUEST)
#

# <img src="path_to_graph">
