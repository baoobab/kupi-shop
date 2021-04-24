from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class PayForm(FlaskForm):
    tttle = StringField('Введите номер банковской карты',
                        validators=[DataRequired()])
    submit2 = SubmitField('Оплата')
