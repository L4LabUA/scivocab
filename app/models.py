from app import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id  = db.Column(db.String(64), index=True, unique=True)
    proctor = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.child_id)   

