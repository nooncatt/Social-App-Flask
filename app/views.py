from . import app


@app.route("/")
def index():
    return "<h1>hello world</h1>"
