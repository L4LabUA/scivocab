from glob import glob
from itertools import zip_longest
from enum import Enum, auto
from pathlib import Path
from pandas import read_excel
import random
import translate
from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    jsonify,
)


ALL_TARGETS_DF = read_excel(
    "static/scivocab/sv_taskdev_imagelist.xlsx",
    sheet_name="all targets",
    index_col=0,
)

# Flask blueprints help keep webapps modular.
bp = Blueprint("scivocab", __name__)


# Saves image file-name. Splits file name to understand separate pieces.
class Image(object):
    def __init__(self, filename):
        self.filename = "/".join(filename.split("/")[1:])
        self.type = str(Path(filename).stem).split("_")[-1]
        self.position = str(Path(filename).stem).split("_")[-2]


#

# class Word(object):
    # def __init__(self, n):
        # self.padded_string = str(n).zfill(3)
        # self.image_list = [
            # Image(filename)
            # for filename in glob(
                # f"static/scivocab/sv_bv1/bv1_b{self.padded_string}*.jpg"
            # )
        # ]
        # self.image_type_dict = {img.type: img for img in self.image_list}
        # self.image_position_dict = {
            # img.position: img for img in self.image_list
        # }
        # self.tw = ALL_TARGETS_DF.loc[f"b{self.padded_string}"]["tw"]


# Get all the words.
WORDS = translate.main("static/scivocab/sv_bv1_input.csv")
# NUMBER_OF_WORDS = int(len(ALL_IMAGES) / 4)
# WORDS = [Word(n) for n in range(1, NUMBER_OF_WORDS + 1)]
strand1 = []
strand2 = []
strand3 = []
strand4 = []
for x in WORDS:
    if WORDS[x].strand == 40:
        strand1.append(x)
    if WORDS[x].strand == 50:
        strand2.append(x)
    if WORDS[x].strand == 62:
        strand3.append(x)
    if WORDS[x].strand == 63:
        strand4.append(x)
random.shuffle(strand1)
random.shuffle(strand2)
random.shuffle(strand3)
random.shuffle(strand4)
randomlist = strand1 + strand2 + strand3 + strand4
# Before I forget what this is- we use this in selectImage to put the images in a random order.
word_type_list = ['tw', 'fp', 'fx', 'fs']

@bp.route("/")
def main():
    current_word = randomlist[0]
    return render_template("index.html", current_word=current_word)


@bp.route("/selectImage", methods=["GET", "POST"])
def selectImage():
    # clicked_image_position = request.args.get("position")
    # Is position being used?
    random.shuffle(word_type_list)
    word_index = int(request.args.get("word_index", 0))
    current_word = randomlist[word_index]
    # Define a dictionary- response. Debug purposes.
    # New response format for constructing data
    response = {
        #f"p{n}_filename": current_word.image_position_dict[f"p{n}"].filename
        f"p{n}_filename": translate.toimage(WORDS[current_word], word_type_list[n-1])
        for n in range(1, 5)
    }
    response["tw"] = current_word
    # Append response to result.
    # Dataframe.append - works for dictionaries.
    return jsonify(response)
