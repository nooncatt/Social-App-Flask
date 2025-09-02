from . import app, USERS, POSTS


@app.route("/")
def index():
    response = (
        f"<h1>Hello world</h1>"
        f"USERS:<br>{'<br>'.join([user.repr() for user in USERS])}<br>"
        f"POSTS:<br>{'<br>'.join([post.repr() for post in POSTS])}<br>"
    )
    return response
