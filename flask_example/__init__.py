# coding=utf-8
from urllib.parse import unquote

from flask import Flask, url_for, redirect, request, abort, make_response, jsonify, render_template
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import BaseConverter
from werkzeug.wrappers import Response

from flask_example.db.orm import db

import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import get_debug_queries
from flask_example.utils.utils import get_file_path

app = Flask(__name__, static_folder="./static", template_folder="./template")
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


app.url_map.converters['list'] = ListConverter


# 定义正则转换器的类
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JsonResponse, cls).force_type(response, environ)


app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {"/i/": get_file_path()})
app.response_class = JsonResponse
db.init_app(app)


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


with app.test_request_context():
    print(url_for("list3", page_names="zx"))


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
    # res = make_response(render_template("qwer.html"))
    # return res
    return render_template("qwer.html"), 200


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config["DATABASE_QUERY_TIMEOUT"]:
            app.logger.warn(
                ("Context:{}\nSlow QUERY:{}\nParameters: {}\nDuration: {}\n".format(
                    query.context, query.statement, query.parameters, query.duration))
            )
    return response
