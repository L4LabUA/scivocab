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
    g
)
import pandas as pd
from dataclasses import dataclass, asdict
from app.translate import construct_word_dict, get_filename
from pathlib import Path
from app.models import Proctor, Child, Session
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
        strands = [
            [x for x in self.words if self.words[x].strand == n]
            for n in (40, 50, 62, 63)
        ]

        for strand in strands:
            shuffle(strand)

        # Shuffles the words in each strand, and concatenates each strand in a
        # list self.randomized_list.  Then it creates a list where we store the
        # user inputs (which starts as an empty list, self.answers) and
        # self.word_types, which we will use later.
        self.randomized_list = chain(*strands)
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
# image, and adds the selected word to manager.answers as an instance of the Answer
# class In doing so, it slowly iterates through the list RANDOMIZED_LIST, and
# moves on to a new page when we reach the last word. In the process of ending,
# it should call postprocessing(manager.answers).
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
            answer = Answer(
                    manager.current_word,
                    response_class,
                    manager.words[manager.current_word].strand,
            )

            info(answer)
            manager.answers.append(answer)

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
        # Create a pandas DataFrame with the answer data.
        df = pd.DataFrame([asdict(answer) for answer in manager.answers])

        # Save the dataframe as an Excel workbook with the filename
        # 'answers.xlsx'. This will overwrite any existing file with that name.
        df.to_excel("answers.xlsx")

        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        return jsonify({"redirect": "redirect"})
