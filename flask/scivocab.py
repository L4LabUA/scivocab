from glob import glob
from itertools import zip_longest
from enum import Enum, auto
from pathlib import Path
from pandas import read_excel
from flask import (
    Blueprint,
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    jsonify,
)





def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


ALL_TARGETS_DF = read_excel(
    "static/scivocab/sv_taskdev_imagelist.xlsx",
    sheet_name="all targets",
    index_col=0,
)

bp = Blueprint("scivocab", __name__)


class Image(object):
    def __init__(self, filename):
        self.filename = "/".join(filename.split("/")[1:])
        self.type = str(Path(filename).stem).split("_")[-1]
        self.position = str(Path(filename).stem).split("_")[-2]


class Word(object):
    def __init__(self, n):
        self.padded_string = str(n).zfill(3)
        self.image_list = [
            Image(filename)
            for filename in glob(
                f"static/scivocab/sv_bv1/bv1_b{self.padded_string}*.jpg"
            )
        ]
        self.image_type_dict = {img.type: img for img in self.image_list}
        self.image_position_dict = {
            img.position: img for img in self.image_list
        }
        self.tw = ALL_TARGETS_DF.loc[f"b{self.padded_string}"]["tw"]


# Get all the words.
ALL_IMAGES = glob("static/scivocab/sv_bv1/*.jpg")
NUMBER_OF_WORDS = int(len(ALL_IMAGES) / 4)
WORDS = [Word(n) for n in range(1, NUMBER_OF_WORDS + 1)]


@bp.route("/")
def main():
    current_word = WORDS[0]
    return render_template("index.html", current_word=current_word)


@bp.route("/selectImage", methods=["GET", "POST"])
def selectImage():
    clicked_image_position = request.args.get("position")
    word_index = int(request.args.get("word_index", 0))
    current_word = WORDS[word_index]
    response = {
        f"p{n}_filename": current_word.image_position_dict[f"p{n}"].filename
        for n in range(1, 5)
    }
    response["tw"] = current_word.tw
    return jsonify(response)
