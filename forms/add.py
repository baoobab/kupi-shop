from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired()])
    rate = IntegerField('Оценка 0-5', validators=[DataRequired()])
    cost = IntegerField('Цена (без пробелов)', validators=[DataRequired()])
    image = FileField('Картинка', validators=[DataRequired()])
    submit = SubmitField('Добавить')
