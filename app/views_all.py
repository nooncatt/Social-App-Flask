from . import app, USERS, POSTS


@app.route("/")
def index():
    response = f"<h1>Hello world</h1>{USERS}<br>{POSTS}<br>"
    return response
