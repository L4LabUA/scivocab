from pathlib import Path
from random import shuffle
from itertools import chain
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)


# Flask blueprints help keep webapps modular.
bp = Blueprint("depth", __name__)
