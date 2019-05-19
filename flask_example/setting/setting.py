DEBUG = True
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