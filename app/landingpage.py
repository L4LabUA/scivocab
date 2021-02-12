import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.forms import LoginForm
from app import db
from app.models import Child, Proctor, Session
from datetime import datetime
from uuid import uuid4
from flask_login import current_user, login_user, logout_user
from app.models import Proctor, Child, Session

#this might be useful later when we want to store user names and passwords
#from flaskr.db import get_db

bp = Blueprint("landingpage", __name__)

@bp.route("/", methods=["GET", "POST"])
def main():
    if current_user.is_authenticated:
        #return redirect(url_for('landingpage.main'))
        return render_template("landingpage.html")
    form = LoginForm()
               
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.child_id.data, form.remember_me.data))

        child_id = form.child_id.data
        proctor_id = form.proctor_id.data


        # Check if the child is in the database - if they are not, then add
        # them. We might want to change this behavior later so that if they are
        # not in the database, we do not allow them to log in.
        if Child.query.filter_by(child_id = child_id).first() is None:
            child = Child(child_id = child_id)
            db.session.add(child)
            db.session.commit()

        # Check if the proctor is in the database - if they are not, then add
        # them. We might want to change this behavior later so that if they are
        # not in the database, we do not allow them to log in.
        if Proctor.query.filter_by(proctor_id = proctor_id).first() is None:
            proctor = Proctor(proctor_id = proctor_id)
            db.session.add(proctor)
            db.session.commit()

        session = Session(session_id = str(uuid4()), child_id = child_id, proctor_id = proctor_id)
        db.session.add(session)
        db.session.commit()
        child = Child.query.filter_by(child_id=child_id).first()
        login_user(child, remember=True)
        return render_template('landingpage.html')
    return render_template('login.html', title='Login', form=form)

@bp.route('/home')
def landingpage():
    logout_user()
    return render_template('landingpage.html')
