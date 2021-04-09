from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

# TODO do all the strings need to be 64 characters long? Can we omit the
# lengths?


class Proctor(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class Child(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)
    breadth_task_responses = db.relationship(
        "BreadthTaskResponse", backref="child"
    )
    current_breadth_task_word_id = db.Column(
        db.String(64), db.ForeignKey("word.id")
    )
    current_depth_task_word_id = db.Column(
        db.String(64), db.ForeignKey("word.id")
    )
    current_depth_task_word_id = db.Column(
        db.String(64), db.ForeignKey("word.id")
    )


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_timestamp = db.Column(db.DateTime, default=datetime.now)
    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))


class BreadthTaskImageType(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class DepthTaskImageType(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class DepthTaskImagePosition(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class BreadthTaskImagePosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Strand(db.Model):
    id = db.Column(db.String, primary_key=True)


class Word(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    target = db.Column(db.String)
    breadth_id = db.Column(db.String(64))

    depth_id = db.Column(db.String(64))
    strand_id = db.Column(db.Integer, db.ForeignKey("strand.id"))
    strand = db.relationship("Strand", backref=db.backref("words"), lazy=True)
    audio_file = db.Column(db.String(64), unique=True)


class BreadthTaskImage(db.Model):
    """A class that stores all the information needed to make one set of images
    associated with a target for the breadth task."""

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))
    filename = db.Column(db.String(64), primary_key=True)
    image_type_id = db.Column(
        db.String(64),
        db.ForeignKey("breadth_task_image_type.id"),
        nullable=False,
    )
    image_type = db.relationship(
        "BreadthTaskImageType", backref=db.backref("images"), lazy=True
    )


class DepthTaskImage(db.Model):
    """A class that stores all the information needed to make one set of images
    associated with a target for the depth task."""

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))
    filename = db.Column(db.String(64), primary_key=True)
    image_type_id = db.Column(
        db.String(64),
        db.ForeignKey("depth_task_image_type.id"),
        nullable=False,
    )
    image_type = db.relationship(
        "DepthTaskImageType", backref=db.backref("images"), lazy=True
    )


class BreadthTaskResponse(db.Model):
    """A class that represents a single response in the breadth task."""

    id = db.Column(db.Integer, primary_key=True)

    target_word = db.Column(db.String(64), db.ForeignKey("word.id"))

    # The type of response the subject selected
    response_type = db.Column(
        db.String(64), db.ForeignKey("breadth_task_image_type.id")
    )

    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    position = db.Column(db.String(64))


class DepthTaskResponse(db.Model):
    """A class that represents a single response in the depth task."""

    id = db.Column(db.Integer, primary_key=True)

    target_word = db.Column(db.String(64), db.ForeignKey("word.id"))

    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    image_0 = db.Column(
        db.String(64),
        db.ForeignKey("depth_task_image.filename"),
        nullable=False,
    )
    image_1 = db.Column(
        db.String(64),
        db.ForeignKey("depth_task_image.filename"),
        nullable=False,
    )
    image_2 = db.Column(
        db.String(64),
        db.ForeignKey("depth_task_image.filename"),
        nullable=False,
    )
    image_3 = db.Column(
        db.String(64),
        db.ForeignKey("depth_task_image.filename"),
        nullable=False,
    )


class DefinitionTaskResponse(db.Model):
    """A class that represents a single response in the definition task."""

    id = db.Column(db.Integer, primary_key=True)

    target_word = db.Column(db.String(64), db.ForeignKey("word.id"))

    child_id = db.Column(db.String(64), db.ForeignKey("child.id"))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # The text of the child's response
    text = db.Column(db.String(300), nullable=False)


@login_manager.user_loader
def load_user(id):
    return Child.query.get(id)
