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
    BreadthTaskResponse,
    BreadthTaskImage,
    BreadthTaskImageType,
)
from app import db
from flask_login import login_required, current_user
import logging
from logging import info
from app.TaskManager import TaskManager


class BreadthTaskManager(TaskManager):
    def __init__(self):
        super().__init__("breadth")
        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in BreadthTaskImageType.query.all()]
        self.position_labels = {
            0: "top_left",
            1: "top_right",
            2: "bottom_left",
            3: "bottom_right",
        }

        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in BreadthTaskImageType.query.all()]


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

    # If there isn't a BreadthTaskManager for the current user yet, create one
    # and add it to the MANAGERS dictionary.
    if MANAGERS.get(current_user.id) is None:
        MANAGERS[current_user.id] = BreadthTaskManager()
    return render_template("breadth.html", title="Breadth Task")


@bp.route("/fun_fact/<fun_fact_index>")
@login_required
def redirect_to_fun_fact(fun_fact_index):
    image = url_for(
        "static",
        filename=f"scivocab/women_scientist_images/b_flossie{fun_fact_index}.gif",
    )

    is_final = True if int(fun_fact_index)==4 else False
    print(fun_fact_index, is_final)

    return render_template(
        "fun_fact.html", image=image, task_id="breadth", is_final=is_final
    )


# Each call of nextWord loads a new word, waits for the user to select an
# image, and adds the selected word to manager.answers as an instance of the
# BreadthTaskResponse class.
@bp.route("/nextWord", methods=["GET", "POST"])
@login_required
def nextWord():
    """This endpoint is queried from the frontend to obtain the filenames of
    the images to display for the breadth task."""
    # If the request contains position information, it is from an image click
    # rather than a page load/reload, and so we extract the position of the
    # image that was clicked.
    manager = MANAGERS[current_user.id]
    if request.args.get("position") is not None:
        position = int(request.args.get("position").split("_")[1])
        breadth_task_response = BreadthTaskResponse(
            target_word=manager.current_word.target,
            response_type=manager.image_types[position],
            child_id=current_user.id,
            position=manager.position_labels[position],
        )
        db.session.add(breadth_task_response)
        db.session.commit()

        # We attempt to go to the next word. If a StopIteration exception is
        # raised, that means we are at the end of the list, and so we redirect the
        # user to the post-breadth-task page.
        try:
            manager.go_to_next_word()

            # If the current_word_index is in cumulative_word_counts then we redirect
            if (
                manager.current_word_index
                in manager.cumulative_word_counts
            ):
                manager.current_phase_index += 1
                # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
                # function here. This is our workaround.
                return jsonify(
                    {"redirect": "fun_fact/" + str(manager.current_phase_index)}
                )

        except StopIteration:
            manager.current_phase_index += 1
            return jsonify(
                {"redirect": "fun_fact/" + str(manager.current_phase_index)}
            )



    # We gather the filenames for the browser.
    filename_dict = {
        img.image_type.id: request.script_root
        + "/static/scivocab/images/breadth/"
        + img.filename
        for img in BreadthTaskImage.query.filter_by(
            word_id=manager.current_word.id
        ).all()
    }

    filenames = [
        filename_dict[image_type] for image_type in manager.image_types
    ]

    # We construct a JSON-serializable dictionary with the filenames and the
    # target word.
    if manager.current_word.audio_file is None:
        audio_file = ""
    else:
        audio_file = manager.current_word.audio_file
    response = {
        "filenames": filenames,
        "current_target_word": manager.current_word.target,
        "audio_file": url_for(
            "static", filename="scivocab/audio/" + audio_file
        ),
    }

    # We convert the dictionary into a JSON message using Flask's 'jsonify'
    # function and return that as a response, which will trigger the webpage to
    # change the images displayed with new ones based on this message.
    return jsonify(response)
