from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


class Proctor(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class Child(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True)
    sessions = db.relationship(
        "Session", backref="child", passive_deletes=True
    )
    breadth_responses = db.relationship(
        "BreadthResponse", backref="child", passive_deletes=True
    )
    depth_responses = db.relationship(
        "DepthResponse", backref="child", passive_deletes=True
    )
    definition_responses = db.relationship(
        "DefinitionResponse", backref="child", passive_deletes=True
    )


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_timestamp = db.Column(db.DateTime, default=datetime.now)
    child_id = db.Column(
        db.String(64),
        db.ForeignKey("child.id", ondelete="CASCADE"),
    )
    proctor_id = db.Column(db.String(64), db.ForeignKey("proctor.id"))


class BreadthImageType(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class DepthImageType(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class DepthImagePosition(db.Model):
    id = db.Column(db.String(64), primary_key=True)


class BreadthImagePosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Strand(db.Model):
    id = db.Column(db.String, primary_key=True)


class Word(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    target = db.Column(db.String)

    breadth_id = db.Column(db.String(64))
    depth_id = db.Column(db.String(64))
    definition_id = db.Column(db.String(64))

    strand_id = db.Column(db.Integer, db.ForeignKey("strand.id"))
    strand = db.relationship("Strand", backref=db.backref("words"), lazy=True)
    audio_file = db.Column(db.String(64), unique=True)


class BreadthImage(db.Model):
    """A class that stores all the information needed to make one set of images
    associated with a target for the breadth task."""

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))
    filename = db.Column(db.String(64), primary_key=True)
    image_type_id = db.Column(
        db.String(64),
        db.ForeignKey("breadth_image_type.id"),
        nullable=False,
    )
    image_type = db.relationship(
        "BreadthImageType", backref=db.backref("images"), lazy=True
    )


class DepthImage(db.Model):
    """A class that stores all the information needed to make one set of images
    associated with a target for the depth task."""

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))
    filename = db.Column(db.String(64), primary_key=True)
    image_type_id = db.Column(
        db.String(64),
        db.ForeignKey("depth_image_type.id"),
        nullable=False,
    )
    image_type = db.relationship(
        "DepthImageType", backref=db.backref("images"), lazy=True
    )


class BreadthResponse(db.Model):
    """A class that represents a single response in the breadth task."""

    id = db.Column(db.Integer, primary_key=True)

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))

    # The type of response the subject selected
    response_type = db.Column(
        db.String(64), db.ForeignKey("breadth_image_type.id")
    )

    child_id = db.Column(
        db.String(64),
        db.ForeignKey("child.id", ondelete="CASCADE"),
    )
    timestamp = db.Column(db.DateTime, default=datetime.now)
    position = db.Column(db.String(64))


class DepthResponse(db.Model):
    """A class that represents a single response in the depth task."""

    id = db.Column(db.Integer, primary_key=True)

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))

    child_id = db.Column(
        db.String(64),
        db.ForeignKey("child.id", ondelete="CASCADE"),
    )
    timestamp = db.Column(db.DateTime, default=datetime.now)
    image_0 = db.Column(
        db.String(64),
        db.ForeignKey("depth_image.filename"),
        nullable=False,
    )
    image_1 = db.Column(
        db.String(64),
        db.ForeignKey("depth_image.filename"),
        nullable=False,
    )
    image_2 = db.Column(
        db.String(64),
        db.ForeignKey("depth_image.filename"),
        nullable=False,
    )
    image_3 = db.Column(
        db.String(64),
        db.ForeignKey("depth_image.filename"),
        nullable=False,
    )


class DefinitionResponse(db.Model):
    """A class that represents a single response in the definition task."""

    id = db.Column(db.Integer, primary_key=True)

    word_id = db.Column(db.String(64), db.ForeignKey("word.id"))

    child_id = db.Column(
        db.String(64),
        db.ForeignKey("child.id", ondelete="CASCADE"),
    )
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # The text of the child's response
    text = db.Column(db.String(300), nullable=False)

    # Scores can be 0, 1, 2, 3, or 4
    score = db.Column(db.Integer)


@login_manager.user_loader
def load_user(id):
    return Child.query.get(id)
