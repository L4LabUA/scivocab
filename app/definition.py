import itertools
from random import shuffle
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    g,
    current_app,
    url_for,
)
import json
from app.models import (
    Word,
    Strand,
    DefinitionTaskResponse,
)
from app import db
from app.TaskManager import TaskManager
from flask_login import login_required, current_user
import logging
from logging import info


class DefinitionTaskManager(TaskManager):
    def __init__(self):
        super().__init__("definition")

    def go_to_next_word(self):
        # Set the current_word attribute of the class instance to the next Word
        # in the iterator.
        self.current_word = next(self.randomized_word_iterator)
        self.current_word_index += 1


# We create a Flask blueprint object. Flask blueprints help keep apps modular.
# So in principle, the same blueprint could be used for multiple apps.
bp = Blueprint("definition", __name__)


# Create a global dictionary of managers, keyed by the current user's ID (i.e.
# the child ID)
MANAGERS = {}


@bp.route("/")
@login_required
def main():
    """The main view function for the definition task."""

    # If there isn't a DefinitionTaskManager for the current user yet, create one
    # and add it to the MANAGERS dictionary.
    if MANAGERS.get(current_user.id) is None:
        MANAGERS[current_user.id] = DefinitionTaskManager()
    return render_template("definition.html", title="Definition Task")


@bp.route("/fun_fact/<fun_fact_index>")
@login_required
def redirect_to_fun_fact(fun_fact_index):
    image = url_for(
        "static",
        filename=f"scivocab/women_scientist_images/def_kalpana{fun_fact_index}.gif",
    )
    return render_template("fun_fact.html", image=image, task_id="definition")


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
            text=request.args["response"],
        )
        db.session.add(definition_task_response)
        db.session.commit()

        # We attempt to go to the next word.
        manager.go_to_next_word()
        # if the current_word_index is in strand_word_counts_accumulative the we can redirect
        if (
            manager.current_word_index
            in manager.strand_word_counts_accumulative
        ):
            manager.current_strand_index += 1
            return jsonify(
                {"redirect": "fun_fact/" + str(manager.current_strand_index)}
            )
            # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
            # function here. This is our workaround.

    # We construct a JSON-serializable dictionary with the filenames and the
    # target word.
    response = {
        "current_target_word": manager.current_word.target,
        "audio_file": url_for(
            "static",
            filename="scivocab/audio/" + manager.current_word.audio_file,
        ),
    }

    # We convert the dictionary into a JSON message using Flask's 'jsonify'
    # function and return that as a response, which will trigger the webpage to
    # change the images displayed with new ones based on this message.
    return jsonify(response)
