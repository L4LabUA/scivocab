from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    child_id = StringField("Child ID", validators=[DataRequired()])
    proctor_id = StringField("Proctor", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")
