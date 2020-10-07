from flask import Blueprint
from flask import render_template

bp = Blueprint("landingpage", __name__)

@bp.route("/")
def main():
    return render_template("landingpage.html")

