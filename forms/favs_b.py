from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FavsForm(FlaskForm):
    ttle = StringField('', validators=[DataRequired()])
    submit = SubmitField('\u2713 В избранном')
    # submit2 = SubmitField('Добавить в избранное')
