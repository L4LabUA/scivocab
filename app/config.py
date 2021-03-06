import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SECRET_KEY is used by Flask-wtf to protect webforms against CSRF. I think
    # we will need to set the SECRET_KEY for the enviroment later?
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you will never guess"

    SQLITE3_DB_PATH = os.path.join(basedir, "app.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLITE3_DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
