import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.forms import LoginForm

#this might be useful later when we want to store user names and passwords
#from flaskr.db import get_db

bp = Blueprint("login", __name__)

@bp.route("/", methods=["GET", "POST"])
def main():
        #return render_template("landingpage.html")
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.child_id.data, form.remember_me.data))
        return render_template("landingpage.html")
    return render_template('login.html', title='Login', form=form)
