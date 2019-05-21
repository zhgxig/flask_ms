from flask_example import app
from flask_example.apis.user import user_bp
from flask_example.apis.upload_files import upload_files_bp

if __name__ == "__main__":
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(upload_files_bp, url_prefix="/upload_files")
    from pprint import pprint
    pprint(app.url_map)
    app.run(host="0.0.0.0", port=8000)
