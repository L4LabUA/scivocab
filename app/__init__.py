import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from uuid import uuid4
from .config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    from app.breadth import bp as breadth_bp
    from app.depth import bp as depth_bp
    from app.routes import bp as routes_bp

    """create_app is an an application factory function."""
    scivocab_app = Flask(__name__)
    scivocab_app.config.from_object(Config)
    print(scivocab_app.secret_key)
    db.init_app(scivocab_app)
    db.create_all(app=scivocab_app)  # creates the tables and database

    login_manager.init_app(scivocab_app)
    login_manager.login_view = "routes.login"

    scivocab_app.register_blueprint(routes_bp, url_prefix="/")
    scivocab_app.register_blueprint(breadth_bp, url_prefix="/breadth")
    scivocab_app.register_blueprint(depth_bp, url_prefix="/depth")

    return scivocab_app
