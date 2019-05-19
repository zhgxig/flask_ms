from flask_example import app
from flask_example.apis.user import user_bp

if __name__ == "__main__":
    app.register_blueprint(user_bp, url_prefix="/user")
    from pprint import pprint
    pprint(app.url_map)
    app.run(host="0.0.0.0", port=8000)
