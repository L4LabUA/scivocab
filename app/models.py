from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import enum


class Proctor(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class Child(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now())
    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))


class BreadthTaskImageType(enum.Enum):
    # TODO would be nice to have more informative variable names :(
    tw = 'tw'  # target word
    fp = 'fp'  # phonological foil
    fx = 'fx'  # What is fx???
    fs = 'fs'  # semantic foil


class Strand(enum.Enum):
    forty = '40'
    fifty = '50'
    sixtytwo = '62'
    sixtythree = '63'



def values_callable(x):
    return [e.value for e in x]


# TODO do all the strings need to be 64 characters long? Can we omit the
# lengths?
class Concept(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    breadth_task_id = db.Column(db.String(64), primary_key=True)
    depth_task_id = db.Column(db.String(64))
    strand = db.Column(db.Enum(Strand, values_callable=values_callable))


class BreadthTaskImage(db.Model):
    """A class that stores all the information needed to make one set of images
    associated with a target."""

    target = db.Column(db.String(64), db.ForeignKey("concept.id"))
    filename = db.Column(db.String(64), primary_key=True)
    image_type = db.Column(
        db.Enum(BreadthTaskImageType, values_callable=values_callable)
    )


class BreadthTaskResponse(db.Model):
    """A class that represents a single response in the breadth task."""

    id = db.Column(db.Integer, primary_key=True)

    target_concept = db.Column(db.String(64), db.ForeignKey("concept.id"))

    # The type of response the subject selected
    response_type = db.Column(
        db.Enum(BreadthTaskImageType, values_callable=values_callable)
    )

    # The strand the word belonged to.
    strand = db.Column(db.Enum(Strand))

    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))


@login_manager.user_loader
def load_user(id):
    return Child.query.get(id)
