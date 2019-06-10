from flask import Blueprint, request, jsonify, redirect, url_for
from flask_example.db.model import User
from flask_example.db.orm import db
from flask_example.db.model import LoginUser
import flask_login
user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def index():
    user_name = request.args.get("name")
    user = User(user_name)
    print("User ID: {}".format(user.id))
    db.session().add(user)
    db.session().commit()
    return jsonify({"id": user.id})


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <form action="/user/login, method="POST>
        <input type="text name="name id="name" placeholder="name"></input>
        <input type="password" name="pw" id="pw" placeholder="password"></input>
        <input type="submit name="submit"></input>
        </form>
        """

    name = request.form.get("name")
    pw = request.form.get("pw")
    print(name, pw)
    if pw == "123":
        login_user = LoginUser.query.filter_by(name=name).first()
        if not login_user:
            login_user = LoginUser(name=name)
            db.session.add(login_user)
            db.session.commit()
        flask_login.login_user(login_user)
        return redirect(url_for("user.protected"))
    return "Bad login"


@user_bp.route("/protected")
@flask_login.login_required
def protected():
    user = flask_login.current_user
    return "Logged in as {}| Login_count: {}| IP :{}".format(user.name, user.login_count, user.last_login_ip)

