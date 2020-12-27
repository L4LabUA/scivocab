import os
from random import shuffle
from itertools import chain
from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    jsonify,
    session,
    g,
    current_app,
)
import pandas as pd
from dataclasses import dataclass, asdict
from app.translate import construct_word_dict, get_filename
from pathlib import Path
from app.models import (
    Proctor,
    Child,
    Session,
    Strand,
    BreadthTaskResponse,
    BreadthTaskImage,
    BreadthTaskImageType,
    Word,
)
from app import db
from flask_login import login_required, current_user
import logging
from logging import info


# Set logging level to INFO for debugging purposes
logging.basicConfig(level=logging.INFO)


class BreadthTaskManager(object):
    def initialize(self):

        # Splits the words in self.words into four strands in self.strands, where each strand
        # correlates to the strand types.
        strand_groups = [
            [word for word in self.words if word.strand == strand]
            for strand in Strand.query.all()
        ]

        for strand_group in strand_groups:
            shuffle(strand_group)

        # Shuffles the words in each strand, and concatenates each strand in a
        # list self.randomized_list.  Then it creates a list where we store the
        # user inputs (which starts as an empty list, self.answers) and
        # self.word_types, which we will use later.
        self.randomized_list = chain(*strand_groups)
        self.answers = []

        # We use this in selectImage to put the images in a random order.
        self.word_types = [x.id for x in BreadthTaskImageType.query.all()]

        self.current_word = next(self.randomized_list)

    def go_to_next_word(self, g):
        info("Going to next word")
        # Shuffle the word_types list.
        shuffle(self.word_types)

        # Set the current word
        self.current_word = next(self.randomized_list)

        g.user.set_current_word(self.current_word)


# Flask blueprints help keep webapps modular.
bp = Blueprint("breadth", __name__)


@bp.before_request
def before_request():
    g.user = current_user


# Create a 'bare' instance of BreadthTaskManager
manager = BreadthTaskManager()


@bp.before_app_first_request
def before_app_first_request():
    """Initialize the global BreathTaskManager instance. We have deferred this
    to this function in order for Flask-SQLAlchemy to work."""
    with current_app.app_context():
        manager.initialize()


# Starts the app and leads to a loop of selectImage().
@bp.route("/")
@login_required
def main():
    return render_template(
        "breadth.html", current_word=current_user.get_current_word
    )


@bp.route("/getImageData")
def getImageData():
    response = {
        f"p{n}_filename": get_filename(
            manager.words[manager.current_word], manager.word_types[n - 1]
        )
        for n in range(1, 5)
    }


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
        response_class = manager.word_types[
            int(request.args.get("position")[5]) - 1
        ]
    else:
        response_class = None

    word_index = int(request.args.get("word_index", 0))

    try:
        if response_class is not None:
            breadth_task_response = BreadthTaskResponse(
                target_word=manager.current_word.id,
                response_type=response_class,
                child_id=current_user.id,
            )
            db.session.add(breadth_task_response)
            db.session.commit()

            manager.go_to_next_word(g)

        filenames = [
            img.filename
            for img in BreadthTaskImage.query.filter_by(
                target=manager.current_word.id
            ).all()
        ]

        response = {
            "filenames": ["scivocab/sv_bv1/" + filenames[n]
            for n in range(4)]
        }
        response["tw"] = manager.current_word.id

        return jsonify(response)
    except StopIteration:
        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        return jsonify({"redirect": "redirect"})
