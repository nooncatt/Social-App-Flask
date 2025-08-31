from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects of user type
POSTS = []  # list for objects post type

from . import views_all, models
