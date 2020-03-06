from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField
from wtforms.validators import InputRequired

class BookingForm(FlaskForm):
    clientWeekday = StringField('День недели', [InputRequired()])
    clientTime = StringField('Время', [InputRequired()])
    clientTeacher = StringField('Учитель', [InputRequired()])
    clientName = StringField('Вас зовут', [InputRequired()])
    clientPhone = StringField('Ваш телефон', [InputRequired()])

class RequestForm(FlaskForm):
    goal = RadioField('Какая цель занятий?', choices = [("travel","Для путешествий"),("study","Для школы"),("work","Для работы"),("relocate","Для переезда")])
    time = RadioField('Сколько времени есть?',
                      choices=[("1-2", "1-2 часа внеделю"), ("3-5", "3-5 часов в неделю"), ("5-7", "5-7 часов в неделю"),
                               ("7-10", "7-10 часов в неделю")])
    clientName = StringField('Вас зовут', [InputRequired()])
    clientPhone = StringField('Ваш телефон', [InputRequired()])
