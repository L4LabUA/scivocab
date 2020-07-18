from breadth import bp as breadth_bp
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(breadth_bp, url_prefix="/breadth")
    print(app.url_map)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
