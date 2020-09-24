#original code is # out

#from flask import Blueprint
#from flask import render_template

#bp = Blueprint("login", __name__)


#@bp.route("/")
#def main():
#    return render_template("login.html")

#@bp.route("/login",  methods=["GET", "POST"])
#def login():
#    return

#the path: scivocab/login.py
 
import functools
 
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

#code above might be useful later when we want to store user names and passwords 

        #if error is None:
        return redirect(url_for('landingpage.main'))
    
    return render_template('login.html')
 
 



