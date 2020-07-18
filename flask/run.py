from breadth import bp as breadth_bp
from depth import bp as depth_bp
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(breadth_bp, url_prefix="/breadth")
    app.register_blueprint(depth_bp, url_prefix="/depth")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
