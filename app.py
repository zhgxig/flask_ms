import os
from pprint import pprint

from flask_script import Manager, Server

from flask_example import app
from flask_example.apis.upload_files import upload_files_bp
from flask_example.apis.user import user_bp
from flask_migrate import Migrate, MigrateCommand
from flask_example.db.orm import db
from werkzeug.debug import DebuggedApplication

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(upload_files_bp, url_prefix="/upload_files")

# pprint(app.url_map)

# 迁移
migrate = Migrate(app, db=db)

# debug 调试器
debug_app = DebuggedApplication(app, evalex=True)

# 命令
manager = Manager(app)

manager.add_command("runserver", Server(
    use_reloader=True,
    use_debugger=True,
    host="0.0.0.0",
    port=8000

))

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    # manager.run()
