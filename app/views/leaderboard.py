from .. import app, USERS
from flask import request, Response, url_for
from http import HTTPStatus
import json
import matplotlib.pyplot as plt


@app.get("/users/leaderboard")
def get_users_sorted_leaderboard():  # asc - по возрастанию, desc - по убыванию

    data_type = request.args.get("type")  # "list"
    sort_param = request.args.get("sort")  # "asc/desc"

    if sort_param not in {"asc", "desc"}:
        return Response("Invalid sort (use asc/desc)", HTTPStatus.BAD_REQUEST)

    reverse = sort_param != "asc"

    if len(USERS) == 0:
        return Response("No users on platform", HTTPStatus.NOT_FOUND)

    sorted_users = sorted(USERS, key=lambda u: u.total_reactions, reverse=reverse)

    if data_type == "list":

        payload = {
            "users": [
                {
                    "id": u.id,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "email": u.email,
                    "total_reactions": u.total_reactions,
                }
                for u in sorted_users
            ]
        }

        response = Response(
            json.dumps(payload),
            mimetype="application/json",
            status=HTTPStatus.OK,
        )

        return response

    elif data_type == "graph":
        fig, ax = plt.subplots(figsize=(8, 4))

        reactions_count = [u.total_reactions for u in sorted_users]
        data_users = [f"{u.first_name} {u.last_name}" for u in sorted_users]

        ax.bar(data_users, reactions_count)

        ax.set_ylabel("Number of collected reactions")
        ax.set_title("Users sorted leaderboard by total_reactions")
        plt.xticks(rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.15)
        fig.tight_layout()

        plt.savefig("app/static/leaderboard_graph.png")

        return Response(
            f"<img src= '{url_for('static', filename='leaderboard_graph.png')}'>",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )

    else:
        return Response("Invalid data type", HTTPStatus.BAD_REQUEST)
