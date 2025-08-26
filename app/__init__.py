from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects of user type

from . import views, models
