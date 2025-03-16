from flask import Flask, redirect, url_for

from app.models.sqlite_db_handler import SQLiteDBHandler

from .config import Config
from .models.mongo_db_handler import MongoDBHandler


def create_app():
    app = Flask(__name__)

    sqlite_handler = SQLiteDBHandler(Config.SQLITE_URL)
    app.config["sqlite_handler"] = sqlite_handler

    mongo_handler = MongoDBHandler(Config.MONGO_URL, "AyudaValencia")
    mongo_handler.connect()
    app.config["mongo_handler"] = mongo_handler

    @app.route("/")
    def home():
        return redirect(url_for("home"))

    return app
