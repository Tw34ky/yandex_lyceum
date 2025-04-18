from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = TextAreaField('Содержание работы', validators=[DataRequired()])
    team_leader = StringField("Кто является куратором работы?")
    is_finished = BooleanField("Закончена или нет?")
    collaborations = TextAreaField("С кем вместе будет делаться?")
    duration = DateTimeField("Сколько будет длиться?")
    submit = SubmitField('Применить')
