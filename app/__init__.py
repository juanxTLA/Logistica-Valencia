from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hola mundo, esta es la primerisima version de la app de Valencia"

    return app
