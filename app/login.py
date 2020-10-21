import functools
from forms import LoginForm
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

#this might be useful later when we want to store user names and passwords
#from flaskr.db import get_db

bp = Blueprint("login", __name__)

@bp.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        #subject_name = request.form['Subject Name']
        #proctor_name = request.form['Proctor Name']
        #db = get_db() 
        #error = None

        # The code above might be useful later when we want to store user names and passwords 

        #if error is None:
        return render_template("landingpage.html")

    else:
        form = LoginForm()
        return render_template('login.html', title='Login', form=form)
