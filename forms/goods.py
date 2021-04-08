from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GoodsForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    description = StringField('Краткое описание', validators=[DataRequired()])
    submit = SubmitField('Применить')
