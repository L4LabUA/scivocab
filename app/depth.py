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
    DepthResponse,
    DepthImage,
    DepthImageType,
)
from app import db
from app.TaskManager import TaskManager
from flask_login import login_required, current_user
import logging
from logging import info
from app.common import check_managers_dict


class DepthManager(TaskManager):
    def __init__(self):
        super().__init__("depth")
        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in DepthImageType.query.all()]


# We create a Flask blueprint object. Flask blueprints help keep apps modular.
# So in principle, the same blueprint could be used for multiple apps.
bp = Blueprint("depth", __name__)


# Create a global dictionary of managers, keyed by the current user's ID (i.e.
# the child ID)
MANAGERS = {}


@bp.route("/")
@login_required
def main():
    """The main view function for the depth task."""
    check_managers_dict(MANAGERS, current_user.id, DepthManager)
    return render_template("depth.html", title="Depth Task")


@bp.route("/fun_fact/<fun_fact_index>")
@login_required
def redirect_to_fun_fact(fun_fact_index):
    image = url_for(
        "static",
        filename=f"scivocab/women_scientist_images/d_annie{fun_fact_index}.gif",
    )
    is_final = True if int(fun_fact_index) == 4 else False

    return render_template(
        "fun_fact.html", image=image, task_id="depth", is_final=is_final
    )


# Each call of nextWord loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# DepthResponse class.
@bp.route("/nextWord", methods=["GET", "POST"])
@login_required
def nextWord():
    """This endpoint is queried from the frontend to obtain the filenames of
    the images to display for the depth task."""

    manager = MANAGERS[current_user.id]

    if manager.task_completed:
        return manager.redirect_to_end()

    # If the request contains position information, it is from an image click
    # rather than a page load/reload, and so we extract the position of the
    # image that was clicked.
    if request.args.get("response") is not None:
        images = [
            src.split("/")[-1] for src in json.loads(request.args["response"])
        ]
        print(json.loads(request.args["response"]))
        depth_task_response = DepthResponse(
            word_id=manager.current_word.id,
            child_id=current_user.id,
            image_0=images[0],
            image_1=images[1],
            image_2=images[2],
            image_3=images[3],
        )
        db.session.add(depth_task_response)
        db.session.commit()

        res = manager.check_redirect()
        if res is not None:
            return res

    return manager.make_response(DepthImage)
