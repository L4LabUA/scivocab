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
from flask_login import login_required, current_user
import logging
from logging import info


class DepthTaskManager(object):
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
        depth_training_items = Word.query.filter(
            Word.depth_id.startswith("dt")
        ).all()
        randomized_word_list.extend(depth_training_items)

        # Get the strands from the database
        #excluding training items becuase they have already been added to the list; see above
        strands = [strand for strand in Strand.query.all() if strand.id != "training"]

        # Currently, we randomize the order of the strands.
        shuffle(strands)
        strand_word_counts: list = []

        # For each strand, we shuffle the words in the strand, and add those
        # words to randomized_word_list.
        for strand in strands:
            strand_word_counts.append(len(strand.words))
            words = [
                word for word in strand.words if word.depth_id is not None
            ]
            shuffle(words)
            randomized_word_list.extend(words)

        # create the accumulative count variable
        self.strand_word_counts_accumulative=list(itertools.accumulate(strand_word_counts))


        # Create a list of image types. We will shuffle this list every time we
        # move to a new word in the task, in order to randomize the positions
        # of the four images for a given word.
        self.image_types = [x.id for x in DepthTaskImageType.query.all()]

       
        #Setting current_word_index to -1 so that the two training items are NOT counted
        self.current_word_index = -1 
        self.current_strand_index = 0

       # We create an iterator out of the list in order to have the Python
        # runtime keep track of our iteration and as an additional safeguard to
        # prevent going backwards in the sequence.
        # (https://docs.python.org/3/glossary.html#term-iterator)
        self.randomized_word_iterator = iter(randomized_word_list)

        # We set the 'current_word' property of this instance of the
        # DepthTaskManager class to the next Word object.
        self.current_word = next(self.randomized_word_iterator)

    def go_to_next_word(self):
        # Shuffle the image_types list.
        shuffle(self.image_types)

        # Set the current_word attribute of the class instance to the next Word
        # in the iterator.
        self.current_word = next(self.randomized_word_iterator)
        self.current_word_index += 1

# We create a Flask blueprint object. Flask blueprints help keep apps modular.
# So in principle, the same blueprint could be used for multiple apps.
bp = Blueprint("depth", __name__)


# Create a global dictionary of managers, keyed by the current user's ID (i.e.
# the child ID)
MANAGERS={}


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
    image = url_for("static", filename=f"scivocab/women_scientist_images/d_annie{fun_fact_index}.gif")
    return render_template("fun_fact.html", image=image, task_id_depth = "depth")


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
     
        #if the current_word_index is in strand_word_counts_accumulative the we can redirect
        if manager.current_word_index in manager.strand_word_counts_accumulative:
            manager.current_strand_index+=1
            return jsonify({"redirect": "fun_fact/"+str(manager.current_strand_index)})
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
