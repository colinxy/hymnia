
import os
import datetime
import flask
from flask import Flask
from flask_pymongo import PyMongo

from emotion import best_fit_emotion

app = Flask(__name__)
# mongodb
app.config["MONGO_DBNAME"] = "hymnia"
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
    # print(email)
    user = mongo.db.users.find_one({"email": email})
    print(user)
    # for user in mongo.db.users.find():
    #     print(user)
    return "Here are all the people"


@app.route("/upload", methods=["POST"])
def upload():
    # verify user
    email = flask.request.json["email"]
    username = flask.request.json["username"]
    # mongo.db.users.update_one({
    #     "email": email,
    #     "username": username
    # })

    file = flask.request.files["file"]
    print(file.filename)
    file_binary_str = file.read()

    # save to mongodb
    saved = mongo.db.images.insert_one({
        "filename": file.filename,
        "content": file_binary_str
    })
    saved.inserted_id

    # query ms api
    fit = best_fit_emotion(file_binary_str)
    print(fit)
    if fit is None:
        return {"error": "MS API error"}
    return fit


if __name__ == '__main__':
    IP = "localhost"
    PORT = 8080
    if os.getenv("PRODUCTION"):
        IP = "0.0.0.0"
        PORT = 80
    app.run(IP, PORT)
