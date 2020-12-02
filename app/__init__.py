import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from uuid import uuid4
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from app.breadth import bp as breadth_bp
    from app.depth import bp as depth_bp
    from app.login import bp as login_bp
    """create_app is an an application factory function."""
    scivocab_app = Flask(__name__)
    scivocab_app.config.from_object(Config)
    
    db = SQLAlchemy(scivocab_app)
    db.init_app(scivocab_app)
    db.create_all(app = scivocab_app)
    # migrate.init_app(scivocab_app, db)
    scivocab_app.register_blueprint(login_bp, url_prefix="/")
    scivocab_app.register_blueprint(breadth_bp, url_prefix="/breadth")
    scivocab_app.register_blueprint(depth_bp, url_prefix="/depth")
   
   login = LoginManager(scivocab_app)
   login.init_app(scivocab_app)

   return scivocab_app

from app import models
