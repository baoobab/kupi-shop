from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FavsForm(FlaskForm):
    ttle = StringField('11', validators=[DataRequired()])
    favs_id = IntegerField('23', validators=[DataRequired()])
    submit2 = SubmitField('\u2713 В избранном')
    submit = SubmitField('Добавить в избранное')
