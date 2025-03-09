from flask import Flask

from app.models.sqlite_db_handler import SQLiteDBHandler

from .config import Config


def create_app():
    app = Flask(__name__)

    sqlite_handler = SQLiteDBHandler(Config.SQLITE_URL)
    app.config["sqlite_handler"] = sqlite_handler

    @app.route("/")
    def home():
        return "Hola mundo, esta es la primerisima version de la app de Valencia"

    return app
