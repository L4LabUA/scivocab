from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
)
from app.forms import LoginForm
from app.models import Child, Proctor, Session
from app import db
from flask_login import login_required, login_user, logout_user

bp = Blueprint("routes", __name__)


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("landingpage.html", title="Home")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        child_id = form.child_id.data
        proctor_id = form.proctor_id.data

        # Check if the child is in the database - if they are not, then add
        # them. We might want to change this behavior later so that if they are
        # not in the database, we do not allow them to log in.
        if Child.query.filter_by(id=child_id).first() is None:
            child = Child(id=child_id)
            db.session.add(child)
            db.session.commit()

        # Check if the proctor is in the database - if they are not, then add
        # them. We might want to change this behavior later so that if they are
        # not in the database, we do not allow them to log in.
        if Proctor.query.filter_by(id=proctor_id).first() is None:
            proctor = Proctor(id=proctor_id)
            db.session.add(proctor)
            db.session.commit()

        session_db_entry = Session(
            child_id=child_id, proctor_id=proctor_id
        )
        db.session.add(session_db_entry)
        db.session.commit()

        child = Child.query.filter_by(id=form.child_id.data).first()
        if child is None:
            print("Invalid child_id or password")
            return redirect(url_for("routes.login"))

        login_user(child)
        return redirect(url_for("routes.index"))

    return render_template("login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.index"))
