from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import enum

# TODO do all the strings need to be 64 characters long? Can we omit the
# lengths?


class Proctor(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class Child(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)

    def __init__(self):
        """Initialize the object, set the __current_word property to None"""
        self.__current_word = None

    def set_current_word(self, word: str):
        """Set the current word that the user is on."""
        self.__current_word = word

    def get_current_word(self):
        """Get the current word that the user is on."""
        return self.__current_word


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now())
    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))


class BreadthTaskImageType(enum.Enum):
    # TODO would be nice to have more informative variable names :(
    tw = "tw"  # target word
    fp = "fp"  # phonological foil
    fx = "fx"  # What is fx???
    fs = "fs"  # semantic foil

class BreadthTaskImagePosition(enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4

class Strand(enum.Enum):
    forty = "40"
    fifty = "50"
    sixtytwo = "62"
    sixtythree = "63"


def values_callable(x):
    return [e.value for e in x]


class Word(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    breadth_id = db.Column(db.String(64), unique=True)

    # We will later add depth_id
    depth_id = db.Column(db.String(64))

    strand = db.Column(db.Enum(Strand, values_callable=values_callable))


class BreadthTaskImage(db.Model):
    """A class that stores all the information needed to make one set of images
    associated with a target."""

    target = db.Column(db.String(64), db.ForeignKey("word.id"))
    filename = db.Column(db.String(64), primary_key=True)
    image_type = db.Column(
        db.Enum(BreadthTaskImageType, values_callable=values_callable)
    )


class BreadthTaskResponse(db.Model):
    """A class that represents a single response in the breadth task."""

    id = db.Column(db.Integer, primary_key=True)

    target_word = db.Column(db.String(64), db.ForeignKey("word.id"))

    # The type of response the subject selected
    response_type = db.Column(
        db.Enum(BreadthTaskImageType, values_callable=values_callable)
    )

    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))


@login_manager.user_loader
def load_user(id):
    return Child.query.get(id)
