from datetime import datetime
from app import db

class Proctor(db.Model):
    id = db.Column(db.String(64), primary_key = True, unique = True)

class Child(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True)

class Session(db.Model):
    # We give each session a UUID
    id = db.Column(db.String, primary_key=True)
    datetime = db.Column(db.DateTime, default = datetime.now())
    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))
