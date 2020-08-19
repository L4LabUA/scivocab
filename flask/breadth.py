from glob import glob
from itertools import zip_longest
from enum import Enum, auto
from pathlib import Path
from pandas import read_excel
from random import shuffle
import translate
import answer
import postprocessing
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
bp = Blueprint("breadth", __name__)


# Get all the words.
WORDS = translate.construct_word_dict("static/scivocab/sv_bv1_input.csv")
STRANDS = [
    [x for x in WORDS if WORDS[x].strand == n] for n in (40, 50, 62, 63)
]

for strand in STRANDS:
    shuffle(strand)

RANDOMIZED_LIST = list(chain(*STRANDS))
ANSWERS = list()
# Before I forget what this is- we use this in selectImage to put the images in
# a random order.
WORD_TYPE_LIST = ["tw", "fp", "fx", "fs"]
shuffle(WORD_TYPE_LIST)


@bp.route("/")
def main():
    current_word = RANDOMIZED_LIST[0]
    return render_template("breadth.html", current_word=current_word)

@bp.route("/redirect")
def redirect_to_end():
    return render_template("after.html")

@bp.route("/selectImage", methods=["GET", "POST"])
def selectImage():

    print("position: ", request.args.get("position"))
    response_class = None
    if request.args.get("position") != None:
        response_class = WORD_TYPE_LIST[int(request.args.get("position")[5])-1]
        print('Selected response: ' + WORD_TYPE_LIST[int(request.args.get("position")[5])-1])

    word_index = int(request.args.get("word_index", 0))
    # if word_index is == length of RANDOMIZED_LIST-1
    # Return a new render template for endscreen (Potentially redirect?)
    # Ala: return render_template("breadth.html", current_word=current_word)
    # https://www.kite.com/python/examples/1212/flask-redirect-to-another-url - Render template might be better.

    if word_index >= 3:
        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        return jsonify({"redirect": url_for("breadth.redirect_to_end")})

    current_word = RANDOMIZED_LIST[word_index] # Here's the break
    if current_word == "arachnid":
        postprocessing.toExcel(ANSWERS)
    if response_class!=None:
        ANSWERS.append(answer.Answer(current_word, response_class, WORDS[current_word].strand))
    # New response format for constructing data
    shuffle(WORD_TYPE_LIST)
    response = {
        f"p{n}_filename": translate.get_filename(
            WORDS[current_word], WORD_TYPE_LIST[n - 1]
        )
        for n in range(1, 5)
    }
    response["tw"] = current_word

    # ANSWERS.append = Answer(current_word, )
    # Append response to result.
    # Dataframe.append - works for dictionaries.
    return jsonify(response)
