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
)
import pandas as pd
from dataclasses import dataclass, asdict
from app.translate import construct_word_dict, get_filename
from pathlib import Path
from app.models import Proctor, Child, Session
from app import db
from flask_login import login_required


@dataclass
class Answer:
    """A class that stores all the information needed by the researcher after
    the program is done."""

    # The target word
    word: str

    # The type of response the subject selected (tw, fp, fx, or fs)
    answer: str

    # The strand the word belonged to.
    strand: int


# Flask blueprints help keep webapps modular.
bp = Blueprint("breadth", __name__)

# Imports all words from the given filename and stores them in a dictionary WORDS.
WORDS = construct_word_dict(
    Path(__file__).parents[0] / "static/scivocab/sv_bv1_input.csv"
)

# Splits the words in WORDS into four strands in STRANDS, where each strand
# correlates to the strand types.
STRANDS = [
    [x for x in WORDS if WORDS[x].strand == n] for n in (40, 50, 62, 63)
]

for strand in STRANDS:
    shuffle(strand)

# Shuffles the words in each strand, and concatenates each strand in a list
# RANDOMIZED_LIST.  Then it creates a list where we store the user inputs
# (which starts as an empty list, ANSWERS) and WORD_TYPES, which we will
# use later.
RANDOMIZED_LIST = list(chain(*STRANDS))
ANSWERS = list()

# We use this in selectImage to put the images in a random order.
WORD_TYPES = ["tw", "fp", "fx", "fs"]

# Shuffle the WORD_TYPES list.
shuffle(WORD_TYPES)

# If we are in debug mode, i.e., if the FLASK_DEBUG variable is set to 1, we
# shorten the task to just a few words, for quick development and debugging
# purposes.
if os.environ.get("FLASK_DEBUG") == "1":
    N_WORDS_TO_SHOW = 3
else:
    N_WORDS_TO_SHOW = len(RANDOMIZED_LIST) - 1

# Starts the app and leads to a loop of selectImage().
@bp.route("/")
@login_required
def main():
    current_word = RANDOMIZED_LIST[0]
    return render_template("breadth.html", current_word=current_word)


@bp.route("/redirect")
def redirect_to_end():
    return render_template("after.html")


# Each call of selectImage loads a new word, waits for the user to select an
# image, and adds the selected word to ANSWERS as an instance of the Answer
# class In doing so, it slowly iterates through the list RANDOMIZED_LIST, and
# moves on to a new page when we reach the last word. In the process of ending,
# it should call postprocessing(ANSWERS).
@bp.route("/selectImage", methods=["GET", "POST"])
def select_image():
    response_class = None

    if request.args.get("position"):
        response_class = WORD_TYPES[int(request.args.get("position")[5]) - 1]
        print(
            "Selected response: "
            + WORD_TYPES[int(request.args.get("position")[5]) - 1]
        )

    word_index = int(request.args.get("word_index", 0))

    # If we've reached the last word, we stop and save the answers to Excel.
    if word_index == N_WORDS_TO_SHOW:

        # Create a pandas DataFrame with the answer data.
        df = pd.DataFrame([asdict(answer) for answer in ANSWERS])

        # Save the dataframe as an Excel workbook with the filename
        # 'answers.xlsx'. This will overwrite any existing file with that name.
        df.to_excel("answers.xlsx")

        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        return jsonify({"redirect": "redirect"})

    # Otherwise, return a JSON object with data about the next word to show.
    else:
        current_word = RANDOMIZED_LIST[word_index]  # Here's the break
        if response_class:
            ANSWERS.append(
                Answer(
                    current_word, response_class, WORDS[current_word].strand
                )
            )

        shuffle(WORD_TYPES)

        response = {
            f"p{n}_filename": get_filename(
                WORDS[current_word], WORD_TYPES[n - 1]
            )
            for n in range(1, 5)
        }
        response["tw"] = current_word

        return jsonify(response)
