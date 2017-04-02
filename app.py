
import os
import datetime
import flask
from flask import Flask
from flask_pymongo import PyMongo

from emotion import ms_emotion_api

app = Flask(__name__)
# mongodb
app.config["MONGO_DBNAME"] = "hymnia"
mongo = PyMongo(app)


@app.route("/")
def index():
    return "Welcome to Hymnia"


@app.route("/login", methods=["POST"])
def login():
    """*ignore, not implemented*
    POST JSON to /login, make sure `email` key is present
    """
    req_json = flask.request.json
    print(req_json)

    return "Logged in"


@app.route("/logout")
def logout():
    return "Logged out"


@app.route("/users")
def all_users():
    # email = flask.request.args["email"]
    # print(email)
    mongo.db.users.find()
    return


@app.route("/music")
def all_music():
    return


@app.route("/report")
def report_music():
    email = flask.request.args["email"]
    username = flask.request.args["username"]


@app.route("/upload", methods=["POST"])
def upload():
    """
    `email` and `username` are required as params.
    must send multiparted form with file field set to "file"
    """
    # verify user
    email = flask.request.args["email"]
    username = flask.request.args["username"]

    file = flask.request.files["file"]
    print(file.filename)
    file_bytestr = file.read()

    # query ms api
    emotion = ms_emotion_api(file_bytestr)
    print(emotion)
    if emotion is None:
        return flask.jsonify(error="MS API error, possibly no human face")

    # save to mongodb
    saved = mongo.db.images.insert_one({
        "filename": file.filename,
        "content": file_bytestr,
        "emotion": emotion,
        "date": datetime.datetime.utcnow(),
        "user_email": email,
    })
    # print(saved.inserted_id)
    # create user if needed
    mongo.db.users.update_one(filter={
        "email": email,
    }, update={
        "$set": {"username": username},
        # image_ids: list of foreign ids to images
        "$push": {"image_ids": saved.inserted_id},
    }, upsert=True)

    # client resend image_id when reporting music
    emotion["image_id"] = str(saved.inserted_id)
    return flask.jsonify(emotion)


if __name__ == '__main__':
    IP = "localhost"
    PORT = 8080
    if os.getenv("PRODUCTION"):
        IP = "0.0.0.0"
        PORT = 80
    app.run(IP, PORT)
