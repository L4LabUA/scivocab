from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    child_id = StringField('Child ID', validators=[DataRequired()])
    proctor = StringField('Proctor', validators=[DataRequired()])
    submit = SubmitField('Submit')
