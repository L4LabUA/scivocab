import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess' # SECRET_KEY is used by Flask-wtf to protect webforms against CSRF. I think we will need to set the SECRET_KEY for the enviroment later?


