
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)


@app.route("/")
def index():
    return "Welcome to Hymnia"


if __name__ == '__main__':
    app.run("localhost", 8080)
