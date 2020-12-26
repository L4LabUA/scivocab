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
)
import pandas as pd
from dataclasses import dataclass, asdict
from app.translate import construct_word_dict, get_filename
from pathlib import Path
from app.models import Proctor, Child, Session, Strand, BreadthTaskResponse
from app import db
from flask_login import login_required, current_user
import logging
from logging import info


# Set logging level to INFO for debugging purposes
logging.basicConfig(level=logging.INFO)


class BreadthTaskManager(object):
    def __init__(self):
        # Imports all words from the given filename and stores them in a dictionary
        self.words = construct_word_dict(
            Path(__file__).parents[0] / "static/scivocab/sv_bv1_input.csv"
        )

        # Splits the words in self.words into four strands in self.strands, where each strand
        # correlates to the strand types.
        strand_groups = [
            [x for x in self.words if self.words[x].strand == n]
            for n in [
                int(member.value) for n, member in Strand.__members__.items()
            ]
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
        self.word_types = ["tw", "fp", "fx", "fs"]

        self.current_word = next(self.randomized_list)

    def go_to_next_word(self, g):
        info("Going to next word")
        # Shuffle the word_types list.
        shuffle(self.word_types)

        # Set the current word
        self.current_word = next(self.randomized_list)

        g.user.current_word = self.current_word


# Flask blueprints help keep webapps modular.
bp = Blueprint("breadth", __name__)


@bp.before_request
def before_request():
    g.user = current_user


manager = BreadthTaskManager()

# Starts the app and leads to a loop of selectImage().
@bp.route("/")
@login_required
def main():
    info(manager.current_word)
    return render_template("breadth.html", current_word=manager.current_word)


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
    response_class = None

    if request.args.get("position"):
        response_class = manager.word_types[
            int(request.args.get("position")[5]) - 1
        ]

    word_index = int(request.args.get("word_index", 0))

    try:
        if response_class:
            breadth_task_response = BreadthTaskResponse(
                target_word = manager.current_word,
                response_type = response_class,
                child_id = current_user.id
            )
            db.session.add(breadth_task_response)
            db.session.commit()

        manager.go_to_next_word(g)
        response = {
            f"p{n}_filename": get_filename(
                manager.words[manager.current_word], manager.word_types[n - 1]
            )
            for n in range(1, 5)
        }
        response["tw"] = manager.current_word

        return jsonify(response)
    except StopIteration:
        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        return jsonify({"redirect": "redirect"})
