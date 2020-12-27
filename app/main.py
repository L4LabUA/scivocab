from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import create_app


# Running main.py will launch the local flask server. It will run until
# manually shut down (or it crashes).  While it is running, you can access the
# website at http://127.0.0.1:5000/(page), where page is the website page you
# want to go to, i.e. http://127.0.0.1:5000/breadth.

app = create_app()

if __name__ == "__main__":
    app.run()
