# coding=utf-8
import logging
import os
from logging.handlers import RotatingFileHandler
from urllib.parse import unquote

import flask_login
from flask import Flask, url_for, redirect, request, abort, make_response, jsonify, render_template
from flask import request_finished
from flask_sqlalchemy import get_debug_queries
from werkzeug.middleware.profiler import ProfilerMiddleware
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.routing import BaseConverter
from werkzeug.wrappers import Response

from flask_example.db.orm import db
from flask_example.utils.utils import get_file_path

from flask_debugtoolbar import DebugToolbarExtension

from collections import OrderedDict

app = Flask(__name__, static_folder="./static", template_folder="./templates")
json_page = Flask(__name__)
app.config.from_object("flask_example.setting.setting")

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler("logs/slow_query.log", maxBytes=10000, backupCount=10)

handler.setLevel(logging.WARN)
handler.setFormatter(formatter)
app.logger.addHandler(handler)


class ListConverter(BaseConverter):

    def __init__(self, url_map, separator='+'):
        super(ListConverter, self).__init__(url_map)
        self.separator = unquote(separator)

    def to_python(self, value):
        if "+" in value:
            return value.split(self.separator)

    def to_url(self, values):
        return self.separator.join(BaseConverter.to_url(self, value)
                                   for value in values)


# url 识别
app.url_map.converters['list'] = ListConverter


# 定义正则转换器的类
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# url 识别
app.url_map.converters['regex'] = RegexConverter


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JsonResponse, cls).force_type(response, environ)


app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {"/i/": get_file_path()})

# 将 dict -> json
json_page.response_class = JsonResponse

# 初始化 db
db.init_app(app)

# 登录信号
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# debug tool
toolbar = DebugToolbarExtension()
toolbar.init_app(app)

# 文件服务器
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    "/static/": os.path.join(os.path.dirname(__file__), "static")
})

# profile 性能调试器
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="/profile")
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, OrderedDict((
    ("/json", json_page),
)))


@json_page.route("/hello")
def hello_():
    return {"a": 1, "b": 2}


@app.route("/")
def hello():
    res = make_response("<body></body>")
    res.headers["Content-Type"] = "text/html;charset=utf-8"
    return res


@app.route("/<int:id>/")
def hello_world(id):
    return "Hello world!---{}".format(id)


@app.route('/list1/<list:page_names>/')
def list1(page_names):
    return 'Separator: {} {}'.format('+', page_names)


@app.route('/list2/<list(separator=u"|"):page_names>/')
def list2(page_names):
    return 'Separator: {} {}'.format('|', page_names)


@app.route('/list3/<regex("([a-z]|[A-Z]){4}"):page_names>/')
def list3(page_names):
    return 'regex: {}'.format(page_names)


# with app.test_request_context():
#     print(url_for("list3", page_names="zx"))


@app.route("/list4/")
def list4():
    return redirect(url_for("hello_world", id=29), code=301)


@app.route("/people")
def people():
    name = request.args.get("name")
    if not name:
        return redirect(url_for("login"))
    user_agent = request.headers.get("User-Agent")
    return "Name:{0};UA:{1}".format(name, user_agent)


@app.route("/login")
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        return "User: {} login".format(user_id)
    else:
        return "Open Login page"


@app.route("/secret")
def secret():
    abort(404)
    print("This is never executed!")


@app.errorhandler(404)
def not_found(error):
    resp = make_response("无法发现新大陆!!!抱歉哦", 404)
    return resp


@app.route("/custom_headers")
def headers():
    res = make_response(render_template("qwer.html"))
    res.headers["Content-Type"] = "text/html;charset=utf-8"
    return res


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config["DATABASE_QUERY_TIMEOUT"]:
            app.logger.warn(
                ("Context:{}\nSlow QUERY:{}\nParameters: {}\nDuration: {}\n".format(
                    query.context, query.statement, query.parameters, query.duration))
            )
    return response


# def log_response(sender, response, **extra):
#     sender.logger.debug("Resquest over. Response: {}".format(response.data.decode()))
#
#
# request_finished.connect(log_response, app)


@flask_login.user_logged_in.connect_via(app)
def _track_logins(sender, user, **extra):
    user.login_count += 1
    user.last_login_ip = request.remote_addr
    db.session.add(user)
    db.session.commit()


@login_manager.user_loader
def user_loader(id):
    from flask_example.db.model import LoginUser
    user = LoginUser.query.filter_by(id=id).first()
    return user
