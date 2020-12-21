from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models import Child, Proctor, Session
from uuid import uuid4
from app import db

bp = Blueprint("routes", __name__)

@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("landingpage.html", title="Home")

@bp.route("/login", methods=["GET", "POST"])
def login():
    print('current user authenticated test 1?', current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))

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

        child = Child.query.filter_by(child_id=form.child_id.data).first()
        print('child, form.child_id', child, form.child_id.data)
        if child is None:
            print("Invalid child_id or password")
            return redirect(url_for("routes.login"))
        login_user(child, remember=True)
        print('current user authenticated? test 2', current_user.is_authenticated)
        next_page = request.args.get('next')
        print('next page', next_page)
        if not next_page or url_parse(next_page).netloc != '':
            print("Redirecting to routes.index")
            next_page = url_for('routes.index')
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)




@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.index"))
