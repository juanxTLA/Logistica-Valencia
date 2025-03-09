from flask import Blueprint, jsonify

affected = Blueprint("affected", __name__)


@affected.route("/find")
def find():
    # database = current_app.config["mongo_handler"]
    return jsonify({"message": "find"})
