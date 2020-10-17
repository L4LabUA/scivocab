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

# imports all words from the given filename and stores them in a dictionary WORDS.
WORDS = translate.construct_word_dict("static/scivocab/sv_bv1_input.csv")

# splits the words in WORDS into four strands in STRANDS, where each strand correlates
# to the strand types.
STRANDS = [
    [x for x in WORDS if WORDS[x].strand == n] for n in (40, 50, 62, 63)
]

for strand in STRANDS:
    shuffle(strand)

# shuffles the words in each strand, and concatenates each strand in a list RANDOMIZED_LIST.
# Then it creates a list where we store the user inputs (which starts as an empty list, ANSWERS) and
# WORD_TYPE_LIST, which we will use later.
RANDOMIZED_LIST = list(chain(*STRANDS))
ANSWERS = list()
# we use this in selectImage to put the images in
# a random order.
WORD_TYPE_LIST = ["tw", "fp", "fx", "fs"]
shuffle(WORD_TYPE_LIST)


# starts the webapp up, and leads to a loop of selectImage().
@bp.route("/")
def main():
    current_word = RANDOMIZED_LIST[0]
    return render_template("breadth.html", current_word=current_word)


@bp.route("/redirect")
def redirect_to_end():
    return render_template("after.html")


# each call of selectImage loads a new word, waits for the user to select an image, and
# adds the selected word to ANSWERS in a data format known as answer.
# In doing so, it slowly iterates through the list RANDOMIZED_LIST, and moves on to a new page when we
# reach the last word. In the process of ending, it should call postprocessing(ANSWERS).
@bp.route("/selectImage", methods=["GET", "POST"])
def select_image():
    print("position: ", request.args.get("position"))
    response_class = None
    if request.args.get("position"):
        response_class = WORD_TYPE_LIST[int(request.args.get("position")[5])-1]
        print('Selected response: ' + WORD_TYPE_LIST[int(request.args.get("position")[5])-1])

    word_index = int(request.args.get("word_index", 0))
    # Return a new render template for endscreen (Potentially redirect?)
    # Ala: return render_template("breadth.html", current_word=current_word)
    # https://www.kite.com/python/examples/1212/flask-redirect-to-another-url - Render template might be better.

    if word_index >= 3:  # Here's where it breaks- note, for testing purposes it breaks after three images move through.
        # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
        # function here. This is our workaround.
        postprocessing.toExcel(ANSWERS)
        return jsonify({"redirect": "redirect"})

    current_word = RANDOMIZED_LIST[word_index]  # Here's the break
    if response_class:
        ANSWERS.append(answer.Answer(current_word, response_class, WORDS[current_word].strand))
    shuffle(WORD_TYPE_LIST)
    response = {
        f"p{n}_filename": translate.get_filename(
            WORDS[current_word], WORD_TYPE_LIST[n - 1]
        )
        for n in range(1, 5)
    }
    response["tw"] = current_word
    return jsonify(response)
