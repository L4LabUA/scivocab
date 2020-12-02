from datetime import datetime
from app import db
from flask_login import UserMixin

class Proctor(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key = True, unique = True)

class Child(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True)

class Session(UserMixin, db.Model):
    # We give each session a UUID
    id = db.Column(db.String, primary_key=True)
    datetime = db.Column(db.DateTime, default = datetime.now())
    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))

@login.user_loader
def load_user(id):
    return Proctor.query.get(int(id))

@login.user_loader
def load_user(id):
    return Child.query.get(int(id))

@login.user_loader
def load_user(id):
    return Session.query.get(int(id))
