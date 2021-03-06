DEBUG = False
SECRET_KEY = "QWER"

# mysql
HOSTNAME = "127.0.0.1"
DATABASE = "demo"
USERNAME = "root"
PASSWORD = "example"
DB_URI = "mysql+pymysql://{}:{}@{}/{}".format(USERNAME, PASSWORD, HOSTNAME, DATABASE)

# flask-sqlalchemy
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# sql 慢查询
DATABASE_QUERY_TIMEOUT = 0.00001
SQLALCHEMY_RECORD_QUERIES = True


# 上传文件
UPLOAD_FOLDER = "../upload_files"


# tool
DEBUG_TB_ENABLED = True

# coding
JSON_AS_ASCII = False
JSONIFY_MIMETYPE = "application/json;charset=utf-8"
