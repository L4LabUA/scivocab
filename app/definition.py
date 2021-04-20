from random import shuffle
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    g,
    current_app,
    url_for
)
import json
from app.models import (
    Word,
    Strand,
    DefinitionTaskResponse,
)
from app import db
from flask_login import login_required, current_user
import logging
from logging import info


class DefinitionTaskManager(object):
    def __init__(self):
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

        # training items
        definition_training_items = Word.query.filter(
            Word.definition_id.startswith("deft")
        ).all()
        randomized_word_list.extend(definition_training_items)

        # Currently, we randomize the order of the strands.
        # NOTE: Jessie says that in the future, the order may not be random.
        shuffle(strands)

        # For each strand, we shuffle the words in the strand, and add those
        # words to randomized_word_list.
        for strand in strands:
            words = [
                word for word in strand.words if word.depth_id is not None
            ]
            shuffle(words)
            randomized_word_list.extend(words)

        # We create an iterator out of the list in order to have the Python
        # runtime keep track of our iteration and as an additional safeguard to
        # prevent going backwards in the sequence.
        # (https://docs.python.org/3/glossary.html#term-iterator)
        self.randomized_word_iterator = iter(randomized_word_list)

        # We set the 'current_word' property of this instance of the
        # DefinitionTaskManager class to the next Word object.
        self.current_word = next(self.randomized_word_iterator)

    def go_to_next_word(self):
        # Set the current_word attribute of the class instance to the next Word
        # in the iterator.
        self.current_word = next(self.randomized_word_iterator)


# We create a Flask blueprint object. Flask blueprints help keep apps modular.
# So in principle, the same blueprint could be used for multiple apps.
bp = Blueprint("definition", __name__)


# Create a global dictionary of managers, keyed by the current user's ID (i.e.
# the child ID)
MANAGERS={}

@bp.route("/")
@login_required
def main():
    """The main view function for the definition task."""

    # If there isn't a DefinitionTaskManager for the current user yet, create one
    # and add it to the MANAGERS dictionary.
    if MANAGERS.get(current_user.id) is None:
        MANAGERS[current_user.id] = DefinitionTaskManager()
    return render_template("definition.html", title="Definition Task")


@bp.route("/redirect")
@login_required
def redirect_to_end():
    return render_template("after.html")


# Each call of nextWord loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# DefinitionTaskResponse class.
@bp.route("/nextWord", methods=["GET", "POST"])
@login_required
def nextWord():
    """This endpoint is queried from the frontend to obtain the filenames of
    the images to display for the definition task."""

    manager = MANAGERS[current_user.id]

    # If the request contains position information, it is from an image click
    # rather than a page load/reload, and so we extract the position of the
    # image that was clicked.


    if request.args.get("response") is not None:
        definition_task_response = DefinitionTaskResponse(
            target_word=manager.current_word.target,
            child_id=current_user.id,
            text=request.args["response"]
        )
        db.session.add(definition_task_response)
        db.session.commit()

        # We attempt to go to the next word. If a StopIteration exception is
        # raised, that means we are at the end of the list, and so we redirect the
        # user to the post-definition-task page.
        try:
            manager.go_to_next_word()

        except StopIteration:
            # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
            # function here. This is our workaround.
            return jsonify({"redirect": "redirect"})

    # If the StopIteration exception was not raised, we continue on, telling
    # the browser which images to display, via a JSON message.

    # We construct a JSON-serializable dictionary with the filenames and the
    # target word.
    response = {
        "current_target_word": manager.current_word.target,
        "audio_file": url_for("static", filename= "scivocab/audio/" + manager.current_word.audio_file),
    }

    # We convert the dictionary into a JSON message using Flask's 'jsonify'
    # function and return that as a response, which will trigger the webpage to
    # change the images displayed with new ones based on this message.
    return jsonify(response)
