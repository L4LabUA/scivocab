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
    DefinitionResponse,
)
from app import db
from app.TaskManager import TaskManager
from flask_login import login_required, current_user
import logging
from logging import info
from app.common import check_managers_dict


class DefinitionManager(TaskManager):
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
    check_managers_dict(MANAGERS, current_user.id, DefinitionManager)
    return render_template("definition.html", title="Definition Task")


@bp.route("/fun_fact/<fun_fact_index>")
@login_required
def redirect_to_fun_fact(fun_fact_index):
    image = url_for(
        "static",
        filename=f"scivocab/women_scientist_images/def_kalpana{fun_fact_index}.gif",
    )
    is_final = True if int(fun_fact_index) == 4 else False
    return render_template("fun_fact.html", image=image, task_id="definition", is_final=is_final)


# Each call of nextWord loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# DefinitionResponse class.
@bp.route("/nextWord", methods=["GET", "POST"])
@login_required
def nextWord():
    """This endpoint is queried from the frontend to obtain the filenames of
    the images to display for the definition task."""

    manager = MANAGERS[current_user.id]
    if manager.task_completed:
        return manager.redirect_to_end()

    # If the request contains position information, it is from an image click
    # rather than a page load/reload, and so we extract the position of the
    # image that was clicked.

    if request.args.get("response") is not None:
        definition_task_response = DefinitionResponse(
            word_id=manager.current_word.id,
            child_id=current_user.id,
            text=request.args["response"],
        )
        db.session.add(definition_task_response)
        db.session.commit()


        res = manager.check_redirect()
        if res is not None:
            return res

    return manager.make_response()
