
from flask import Flask
from flask_pymongo import PyMongo
import flask_login

app = Flask(__name__)

# mongodb
mongo = PyMongo(app)

# login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@app.route("/")
def index():
    return "Welcome to Hymnia"


@app.route("/login", methods=["POST"])
def login():
    pass


if __name__ == '__main__':
    app.run("localhost", 8080)
