from glob import glob
from itertools import zip_longest
from enum import Enum, auto
from pathlib import Path
from pandas import read_excel
from random import shuffle
import translate
import answer
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
strands = [
    [x for x in WORDS if WORDS[x].strand == n] for n in (40, 50, 62, 63)
]

for strand in strands:
    shuffle(strand)

randomized_list = list(chain(*strands))
answers = list()

# Before I forget what this is- we use this in selectImage to put the images in
# a random order.
word_type_list = ["tw", "fp", "fx", "fs"]


@bp.route("/")
def main():
    current_word = randomized_list[0]
    return render_template("breadth.html", current_word=current_word)


@bp.route("/selectImage", methods=["GET", "POST"])
def selectImage():
    shuffle(word_type_list)
    word_index = int(request.args.get("word_index", 0))
    current_word = randomized_list[word_index]
    for i in word_type_list:
        print(i)
    print(' ')
    # New response format for constructing data
    response = {
        f"p{n}_filename": translate.get_filename(
            WORDS[current_word], word_type_list[n - 1]
        )
        for n in range(1, 5)
    }
    response["tw"] = current_word
    # answers.append = Answer(current_word, )
    for i in word_type_list:
        print(i)
    print(request.args.get("position"))
    if request.args.get("position") != None:
        print('answer: ' + word_type_list[int(request.args.get("position")[5])-1])
    # Append response to result.
    # Dataframe.append - works for dictionaries.
    # print(response)
    return jsonify(response)
