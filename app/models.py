from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login_manager

class Proctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proctor_id = db.Column(db.String(64), unique = True)

class Child(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.String(64), unique = True)

class Session(UserMixin, db.Model):
    # We give each session a UUID
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, unique=True)
    datetime = db.Column(db.DateTime, default = datetime.now())
    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))

@login_manager.user_loader
def load_user(id):
    return Child.query.get(int(id))
