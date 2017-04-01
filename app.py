
import os
import flask
from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)

# mongodb
mongo = PyMongo(app)


@app.route("/")
def index():
    return "Welcome to Hymnia"


@app.route("/login", methods=["POST"])
def login():
    """POST JSON to /login, make sure `email` key is present"""
    req_json = flask.request.json
    print(req_json)

    return "Logged in"


@app.route("/logout")
def logout():
    return "Logged out"


@app.route("/board")
def board():
    email = flask.request.json["email"]
    user = mongo.db.users.find_one({"email": email})
    print(user)
    return "Here are all the people"


if __name__ == '__main__':
    IP = "localhost"
    PORT = 8080
    if os.getenv("PRODUCTION"):
        IP = "0.0.0.0"
        PORT = 80
    app.run(IP, PORT)
