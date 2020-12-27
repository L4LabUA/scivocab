from itertools import zip_longest
from pathlib import Path
from pandas import read_excel
from random import shuffle
from app.translate import construct_word_dict
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


# Flask blueprints help keep webapps modular.
bp = Blueprint("depth", __name__)


# Imports all words from the given filename and stores them in a dictionary WORDS.
WORDS = construct_word_dict(Path(__file__).parents[0]/"static/scivocab/sv_bv1_input.csv")

strands = [
    [x for x in WORDS if WORDS[x].strand == n] for n in (40, 50, 62, 63)
]

for strand in strands:
    shuffle(strand)

randomized_list = list(chain(*strands))

# Before I forget what this is- we use this in selectImage to put the images in
# a random order.
word_type_list = ["tw", "fp", "fx", "fs"]


@bp.route("/")
def main():
    current_word = randomized_list[0]
    return render_template("depth.html", current_word=current_word)


@bp.route("/nextWord", methods=["GET", "POST"])
def nextWord():
    shuffle(word_type_list)
    word_index = int(request.args.get("word_index", 0))
    current_word = randomized_list[word_index]

    # New response format for constructing data
    response = {
        f"p{n}_filename": translate.get_filename(
            WORDS[current_word], word_type_list[n - 1]
        )
        for n in range(1, 5)
    }
    response["tw"] = current_word

    # Append response to result.
    # Dataframe.append - works for dictionaries.
    return jsonify(response)
