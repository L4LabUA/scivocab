from random import shuffle
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    g,
    current_app,
)
from app.models import (
    Word,
    Strand,
    BreadthTaskResponse,
    BreadthTaskImage,
    BreadthTaskImageType,
)
from app import db
from flask_login import login_required, current_user
import logging
from logging import info


class BreadthTaskManager(object):
    def initialize(self):
        """The code in this method would normally be in the class's __init__
        method. However, we put the logic in this function instead because we
        need a top-level instance of this class to persist across requests in
        order to keep track of which item (word) a user has reached in the
        task, in order to prevent page refreshes/logouts from resetting
        progress.

        The normal method of persisting data across requests with Flask is to
        use Flask's 'session' object. However, this persistence is implemented
        by storing data on the user's computer as a cookie, which means that
        any data that is put into the Flask 'session' object must be
        JSON-serializable. Unfortunately, SQLAlchemy classes are not trivially
        serializable. In principle, we could implement custom serialization and
        deserialization logic, but for expediency's sake, we opt instead to
        keep the instance of the manager in memory rather than reconstructing
        it for every request."""

        # Create an empty list to hold Word objects
        randomized_word_list: list[Word] = []

        # Get the strands from the database
        strands = Strand.query.all()

        # Currently, we randomize the order of the strands.
        # NOTE: Jessie says that in the future, the order may not be random.
        shuffle(strands)

        # For each strand, we shuffle the words in the strand, and add those
        # words to randomized_word_list.
        for strand in strands:
            shuffle(strand.words)
            randomized_word_list.extend(strand.words)

        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in BreadthTaskImageType.query.all()]

        # We create an iterator out of the list in order to have the Python
        # runtime keep track of our iteration and as an additional safeguard to
        # prevent going backwards in the sequence.
        # (https://docs.python.org/3/glossary.html#term-iterator)
        self.randomized_word_iterator = iter(randomized_word_list)

        # We set the 'current_word' property of this instance of the
        # BreadthTaskManager class to the next Word object.
        self.current_word = next(self.randomized_word_iterator)

    def go_to_next_word(self):
        # Shuffle the image_types list.
        shuffle(self.image_types)

        # Set the current_word attribute of the class instance to the next Word
        # in the iterator.
        self.current_word = next(self.randomized_word_iterator)

        current_user.set_current_word(self.current_word)


# We create a Flask blueprint object. Flask blueprints help keep apps modular.
# So in principle, the same blueprint could be used for multiple apps.
bp = Blueprint("breadth", __name__)


# Create a 'bare' instance of BreadthTaskManager
manager = BreadthTaskManager()


@bp.before_app_first_request
def before_app_first_request():
    """Initialize the global BreathTaskManager instance. We have deferred this
    to this function in order for Flask-SQLAlchemy to work."""
    with current_app.app_context():
        manager.initialize()


@bp.route("/")
@login_required
def main():
    return render_template("breadth.html")


@bp.route("/redirect")
def redirect_to_end():
    return render_template("after.html")


# Each call of selectImage loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# BreadthTaskResponse class.
@bp.route("/selectImage", methods=["GET", "POST"])
def select_image():

    # If the request contains position information, it is from an image click
    # rather than a page load/reload.
    if request.args.get("position"):
        response_class = manager.image_types[
            int(request.args.get("position")[5])
        ]
    else:
        response_class = None

    try:
        if response_class is not None:
            breadth_task_response = BreadthTaskResponse(
                target_word=manager.current_word.id,
                response_type=response_class,
                child_id=current_user.id,
            )
            db.session.add(breadth_task_response)
            db.session.commit()

            manager.go_to_next_word()

        filenames = [
            img.filename
            for img in BreadthTaskImage.query.filter_by(
                target=manager.current_word.id
            ).all()
        ]

        response = {
            "filenames": ["scivocab/sv_bv1/" + filenames[n] for n in range(4)]
        }
        response["tw"] = manager.current_word.id

        return jsonify(response)
    except StopIteration:
        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        return jsonify({"redirect": "redirect"})
