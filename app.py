import flask
from flask import Flask, render_template, request
import json
import random
from flask_sqlalchemy import SQLAlchemy
from modules.models import db, TeachersTable, BookingTable, RequestTable
from modules.forms import BookingForm, RequestForm
import ast
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'my-super-secret-phrase-I-dont-tell-this-to-nobody'
db.init_app(app)
app.app_context().push()

goalsdict = {"travel": "Для путешествий", "study": "Для учебы", "work": "Для работы", "relocate": "Для переезда"}

@app.route('/')
def main():
    tutors = db.session.query(TeachersTable).order_by(func.random()).limit(6)
    tutors = [r for r in tutors]  # превращаем в лист
    for i in range(0, len(tutors)):
        tutors[i].goals = ast.literal_eval(tutors[i].goals)
        tutors[i].free = ast.literal_eval(tutors[i].free)
    return render_template('index.html', tutors=tutors, goalsdict=goalsdict)

@app.route('/all')
def all():
    tutors = db.session.query(TeachersTable).all()
    tutors = [r for r in tutors] #превращаем в лист
    for i in range(0, len(tutors)):
        tutors[i].goals = ast.literal_eval(tutors[i].goals)
        tutors[i].free = ast.literal_eval(tutors[i].free)
    return render_template('index.html', tutors=tutors, goalsdict=goalsdict)

@app.route('/goals/<goal>')
def goals(goal):
    tutors = db.session.query(TeachersTable).filter(TeachersTable.goals.contains(goal))
    tutors = [r for r in tutors] #превращаем в лист
    for i in range(0, len(tutors)):
         tutors[i].goals = ast.literal_eval(tutors[i].goals)
         tutors[i].free = ast.literal_eval(tutors[i].free)
    return render_template('goal.html', tutors=tutors, goalsdict=goalsdict, goal=goal)

@app.route('/profile/<tutorid>/')
def profile(tutorid):
    tutor = db.session.query(TeachersTable).get_or_404(tutorid)
    tutor.goals = ast.literal_eval(tutor.goals)
    tutor.free = ast.literal_eval(tutor.free)
    return render_template('profile.html', tutor=tutor, goalsdict=goalsdict)

@app.route('/request/')
def requestpage():
    form = RequestForm()
    return render_template('request.html',form=form)

@app.route('/request_done/', methods=["POST"])
def request_done():
    form = RequestForm()
    studentrequest = RequestTable(goal=form.goal.data,
                           time=form.time.data,
                           clientName=form.clientName.data,
                           clientPhone=form.clientPhone.data
                           )
    db.session.add(studentrequest)
    db.session.commit()

    goal = form.goal.data
    time = form.time.data
    clientName = form.clientName.data
    clientPhone = form.clientPhone.data

    return render_template('request_done.html', goal=goalsdict[goal],
                           time=time, clientName=clientName, clientPhone=clientPhone)

@app.route('/booking/<tutorid>/<dayofweek>/<time>/')
def booking(tutorid, dayofweek, time):
    tutor = db.session.query(TeachersTable).get_or_404(tutorid)
    tutor.goals = ast.literal_eval(tutor.goals)
    tutor.free = ast.literal_eval(tutor.free)

    form = BookingForm()
    return render_template('booking.html', tutor=tutor, dayofweek=dayofweek, time=time, form=form)

@app.route('/booking_done', methods=["POST"])
def booking_done():
    form=BookingForm()
    teacher = BookingTable(clientWeekday = form.clientWeekday.data,
                           clientTime = form.clientTime.data,
                           clientName = form.clientName.data,
                           clientPhone = form.clientPhone.data,
                           teacher_id = int(form.clientTeacher.data)
                            )
    db.session.add(teacher)
    db.session.commit()

    clientWeekday = form.clientWeekday.data
    clientTime = form.clientTime.data
    clientName = form.clientName.data
    clientPhone = form.clientPhone.data
    clientTeacher = int(form.clientTeacher.data)
    return render_template('booking_done.html', clientWeekday=clientWeekday,
                           clientTime=clientTime, clientTeacher=clientTeacher,
                           clientName=clientName, clientPhone=clientPhone)



if __name__ == '__main__':

    app.run()