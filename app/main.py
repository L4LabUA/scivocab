import os
from breadth import bp as breadth_bp
from depth import bp as depth_bp
from login import bp as login_bp
from flask import Flask
from config import Config

# Running main.py will launch the local flask server. It will run until
# manually shut down (or it crashes).  While it is running, you can access the
# website at http://127.0.0.1:5000/(page), where page is the website page you
# want to go to, i.e. http://127.0.0.1:5000/breadth.

def create_app():
    app = Flask(__name__)
    app.register_blueprint(login_bp, url_prefix="/")
    app.register_blueprint(breadth_bp, url_prefix="/breadth")
    app.register_blueprint(depth_bp, url_prefix="/depth")
    app.config.from_object(Config)
    return app

app = create_app()

if __name__ == "__main__":
    app.run()



