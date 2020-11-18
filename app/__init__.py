import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__) #not sure if I need this becuase in main.py
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#from app import routes, models
