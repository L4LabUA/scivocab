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
    DepthTaskResponse,
    DepthTaskImage,
    DepthTaskImageType,
)
from app import db
from app.TaskManager import TaskManager
from flask_login import login_required, current_user
import logging
from logging import info


class DepthTaskManager(TaskManager):
    def __init__(self):
        super().__init__("depth")
        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in DepthTaskImageType.query.all()]


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

    # If there isn't a DepthTaskManager for the current user yet, create one
    # and add it to the MANAGERS dictionary.
    if MANAGERS.get(current_user.id) is None:
        MANAGERS[current_user.id] = DepthTaskManager()

    return render_template("depth.html", title="Depth Task")


@bp.route("/fun_fact/<fun_fact_index>")
@login_required
def redirect_to_fun_fact(fun_fact_index):
    image = url_for(
        "static",
        filename=f"scivocab/women_scientist_images/d_annie{fun_fact_index}.gif",
    )
    return render_template("fun_fact.html", image=image, task_id="depth")


# Each call of nextWord loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# DepthTaskResponse class.
@bp.route("/nextWord", methods=["GET", "POST"])
@login_required
def nextWord():
    """This endpoint is queried from the frontend to obtain the filenames of
    the images to display for the depth task."""

    manager = MANAGERS[current_user.id]

    # If the request contains position information, it is from an image click
    # rather than a page load/reload, and so we extract the position of the
    # image that was clicked.
    if request.args.get("response") is not None:
        images = [
            src.split("/")[-1] for src in json.loads(request.args["response"])
        ]
        depth_task_response = DepthTaskResponse(
            target_word=manager.current_word.target,
            child_id=current_user.id,
            image_0=images[0],
            image_1=images[1],
            image_2=images[2],
            image_3=images[3],
        )
        db.session.add(depth_task_response)
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

    # We gather the filenames for the browser.
    filename_dict = {
        img.image_type.id: request.script_root
        + "/static/scivocab/images/depth/"
        + img.filename
        for img in DepthTaskImage.query.filter_by(
            word_id=manager.current_word.id
        ).all()
    }

    filenames = [
        filename_dict[image_type] for image_type in manager.image_types
    ]

    # We construct a JSON-serializable dictionary with the filenames and the
    # target word.
    response = {
        "filenames": filenames,
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
