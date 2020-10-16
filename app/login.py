from flask import Blueprint
from flask import render_template

bp = Blueprint("login", __name__)

@bp.route("/")
def main():
    return render_template("login.html")
