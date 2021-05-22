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
from app.models import (
    Strand,
    BreadthResponse,
    BreadthImage,
    BreadthImageType,
)
from app import db
from flask_login import login_required, current_user
import logging
from logging import info
from app.TaskManager import TaskManager
from app.common import check_managers_dict


class BreadthManager(TaskManager):
    def __init__(self):
        super().__init__("breadth")
        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in BreadthImageType.query.all()]
        self.position_labels = {
            0: "top_left",
            1: "top_right",
            2: "bottom_left",
            3: "bottom_right",
        }

        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in BreadthImageType.query.all()]


# We create a Flask blueprint object. Flask blueprints help keep apps modular.
# So in principle, the same blueprint could be used for multiple apps.
bp = Blueprint("breadth", __name__)


# Create a global dictionary of managers, keyed by the current user's ID (i.e.
# the child ID)
MANAGERS = {}


@bp.route("/")
@login_required
def main():
    """The main view function for the breadth task."""
    check_managers_dict(MANAGERS, current_user.id, BreadthManager)
    return render_template("breadth.html", title="Breadth Task")


@bp.route("/fun_fact/<fun_fact_index>")
@login_required
def redirect_to_fun_fact(fun_fact_index):
    image = url_for(
        "static",
        filename=f"scivocab/women_scientist_images/b_flossie{fun_fact_index}.gif",
    )

    is_final = True if int(fun_fact_index)==4 else False

    return render_template(
        "fun_fact.html", image=image, task_id="breadth", is_final=is_final
    )


# Each call of nextWord loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# BreadthResponse class.
@bp.route("/nextWord", methods=["GET", "POST"])
@login_required
def nextWord():
    """This endpoint is queried from the frontend to obtain the filenames of
    the images to display for the breadth task."""
    # If the request contains position information, it is from an image click
    # rather than a page load/reload, and so we extract the position of the
    # image that was clicked.
    manager = MANAGERS[current_user.id]
    if manager.task_completed:
        return manager.redirect_to_end()
    if request.args.get("position") is not None:
        position = int(request.args.get("position").split("_")[1])
        breadth_task_response = BreadthResponse(
            word_id=manager.current_word.id,
            response_type=manager.image_types[position],
            child_id=current_user.id,
            position=manager.position_labels[position],
        )
        db.session.add(breadth_task_response)
        db.session.commit()

        res = manager.check_redirect()
        if res is not None:
            return res


    return manager.make_response(BreadthImage)
