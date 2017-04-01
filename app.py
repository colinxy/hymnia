
import os
import flask
from flask import Flask
from flask_pymongo import PyMongo
import flask_login
from flask_login import login_required, LoginManager


app = Flask(__name__)
if os.getenv("SECRET_KEY", None):
    app.secret_key = os.getenv("SECRET_KEY")
else:
    raise ValueError("No SECRET_KEY")

# mongodb
mongo = PyMongo(app)

# login
login_manager = LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    # get user from db
    user_json = mongo.db.users.find({"email": email})
    print(user_json)
    user = User()
    return user


@login_manager.request_loader
def request_loader(request):
    pass


@app.route("/")
def index():
    return "Welcome to Hymnia"


@app.route("/login", methods=["POST"])
def login():
    """POST JSON to /login, make sure `email` key is present"""
    req_json = flask.request.json
    print(req_json)

    # flask_login user object
    user = User()
    user.id = req_json["email"]
    # NO password check: NO password hashing, NO salt
    flask_login.login_user(user)
    return "Logged in"


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"


@app.route("/board")
# @login_required                 # no login needed
def status():
    return "Good to be logged in"


if __name__ == '__main__':
    app.run("localhost", 8080)
