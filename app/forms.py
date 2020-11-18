from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from app.models import User

class LoginForm(FlaskForm):
    child_id = StringField('Child ID', validators=[DataRequired()])
    proctor = StringField('Proctor', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')
