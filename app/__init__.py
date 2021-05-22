from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

# We use the factory pattern. That is, we first create top-level instances of the
# SQLAlchemy and LoginManager classes that are not bound to any application.
# Only later do we associate the instances with an application created using
# the create_app factory function.
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Returns a Flask application instance with our desired blueprints
    and extensions (such as flask_sqlalchemy and flask_login) registered to it."""

    # Import the blueprints
    from app.breadth import bp as breadth_bp
    from app.depth import bp as depth_bp
    from app.definition import bp as definition_bp
    from app.routes import bp as routes_bp

    # Create the app instance
    scivocab_app = Flask(__name__)

    # Configure the app
    scivocab_app.config.from_object(Config)

    # Connect the database to the app
    db.init_app(scivocab_app)

    # Ensure foreign key constraint for SQLite3 (snippet taken from 
    # https://gist.github.com/asyd/a7aadcf07a66035ac15d284aef10d458
    if 'sqlite' in scivocab_app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            print("HELLO")
            dbapi_con.execute('pragma foreign_keys=ON')

        with scivocab_app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)


    # Connect the login manager to the app
    login_manager.init_app(scivocab_app)

    # Tell the login manager where to redirect users if they need to log in.
    # In this instance, they will be redirected to the "/login" endpoint
    # defined in routes.py.
    login_manager.login_view = "routes.login"

    # Register the blueprints
    scivocab_app.register_blueprint(routes_bp, url_prefix="/")
    scivocab_app.register_blueprint(breadth_bp, url_prefix="/breadth")
    scivocab_app.register_blueprint(depth_bp, url_prefix="/depth")
    scivocab_app.register_blueprint(definition_bp, url_prefix="/definition")

    return scivocab_app
