from flask import Blueprint, request, jsonify
from flask_example.db.model import User
from flask_example.db.orm import db


user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def index():
    user_name = request.args.get("name")
    user = User(user_name)
    print("User ID: {}".format(user.id))
    db.session().add(user)
    db.session().commit()
    return jsonify({"id": user.id})
