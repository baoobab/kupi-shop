from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class OrdsForm(FlaskForm):
    ttle = StringField('', validators=[DataRequired()])
    submit = SubmitField('\u2713 В корзине')
    submit2 = SubmitField('Добавить в корзину')
