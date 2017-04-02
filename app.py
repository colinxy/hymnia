
import io
import os
import datetime
from pprint import pprint
import flask
from flask import Flask
import pymongo
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
# from bson import json_util

# youtube streaming
import pafy
import requests

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
    """omit users that haven't uploaded any (image, music)"""
    # TODO: implement pagination
    # skip = flask.request.args["skip"]
    user_cursor = mongo.db.users.find({}, {"_id": False})
    users = []
    for user in user_cursor:
        # pprint(user)
        if "image_ids" in user:
            users.append({
                "username": user["username"],
                "images": [str(im_id) for im_id in user["image_ids"]]
            })
    return flask.jsonify(users)


@app.route("/music")
def all_music():
    return


@app.route("/images")
def all_images():
    image_cursor = mongo.db.images\
        .find({}, {"content": False})\
        .sort("date", pymongo.DESCENDING)
    images = []
    for image in image_cursor:
        # pprint(image)
        if "music" in image:
            images.append({
                "image_id": str(image["_id"]),
                "music": image["music"],
                "filename": image["filename"],
                "emotion": image["emotion"],
                "date": image["date"],
                "username": image["user_username"]
            })
    return flask.jsonify(images)


@app.route("/image/<img_id>")
def get_image(img_id):
    image = mongo.db.images.find_one_or_404({"_id": ObjectId(img_id)})
    print(image["filename"])
    # only handle JPEG for now
    return flask.send_file(io.BytesIO(image["content"]), mimetype="image/jpeg")


@app.route("/report", methods=["POST"])
def report_music():
    # email = flask.request.args["email"]
    # username = flask.request.args["username"]

    image_id = flask.request.json["image_id"]
    music = flask.request.json["music"]
    update = mongo.db.images.update_one({"_id": ObjectId(image_id)},
                                        {"$set": {"music": music}})
    # print(update.raw_result)
    if not update.raw_result["updatedExisting"]:
        flask.abort(404)
    return flask.jsonify(result="success")


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
        "user_username": username,
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


# https://stackoverflow.com/questions/39272072/flask-send-stream-as-response
@app.route("/stream/<youtube_id>")
def stream(youtube_id):
    """Music streaming
    youtube_id: 11 character video id or the URL of the video
    """
    media_type = flask.request.args.get("type", None)
    video = pafy.new(youtube_id)

    if media_type is not None:
        best_audio = video.getbest(preftype=media_type)
    else:
        for typ in ["3gp", "m4a", "mp4", "webm"]:
            best_audio = video.getbest(preftype=typ)
            if best_audio is not None:
                break

    if best_audio is None:
        flask.abort(404)

    # streaming GET
    r = requests.get(best_audio.url, stream=True)
    return flask.Response(r.iter_content(chunk_size=10*1024),
                          content_type=r.headers["Content-Type"])


if __name__ == '__main__':
    IP = "localhost"
    PORT = 8080
    app.run(IP, PORT)
