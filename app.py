import flask
from flask import Flask, render_template
import json
from flask import request
import random

app = Flask(__name__)

f=open('teachers.json','r')
teachers=json.loads(f.read())['teachers']
f.close()


goalsdict = {"travel": "Для путешествий", "study": "Для учебы", "work": "Для работы", "relocate": "Для переезда"}

@app.route('/')
def main():
    tutors=random.sample(teachers, k=6)
    return render_template('index.html', tutors=tutors, goalsdict=goalsdict)

@app.route('/all')
def all():
    return render_template('index.html', tutors=teachers, goalsdict=goalsdict)

@app.route('/goals/<goal>')
def goals(goal):
    tutors = [x for x in teachers if goal in x['goals']]
    return render_template('goal.html', tutors=tutors, goalsdict=goalsdict, goal=goal)

@app.route('/profile/<tutorid>/')
def profile(tutorid):
    tutor = [x for x in teachers if x['id'] == int(tutorid)][0]

    return render_template('profile.html', tutor=tutor, goalsdict=goalsdict)

@app.route('/request/')
def requestpage():
    return render_template('request.html')

@app.route('/request_done/', methods=["POST"])
def request_done():
    goal = request.form.get("goal")
    time = request.form.get("time")
    clientName = request.form.get("clientName")
    clientPhone = request.form.get("clientPhone")
    f = open('request.json', 'a')
    book = {"goal": goal,
            "time": time,
            "clientName": clientName,
            "clientPhone": clientPhone}
    f.write(json.dumps(book))
    return render_template('request_done.html', goal=goal,
                           time=time, clientName=clientName, clientPhone=clientPhone)

@app.route('/booking/<tutorid>/<dayofweek>/<time>/')
def booking(tutorid, dayofweek, time):
    tutor = [x for x in teachers if x['id'] == int(tutorid)][0]
    return render_template('booking.html', tutor=tutor, dayofweek=dayofweek, time=time)

@app.route('/booking_done', methods=["POST"])
def booking_done():
    clientWeekday = request.form.get("clientWeekday")
    clientTime = request.form.get("clientTime")
    clientTeacher = int(request.form.get("clientTeacher"))
    clientName = request.form.get("clientName")
    clientPhone = request.form.get("clientPhone")
    f = open('booking.json', 'a')
    book={"clientWeekday":clientWeekday,
          "clientTime":clientTime,
          "clientTeacher":clientTeacher,
          "clientName":clientName,
          "clientPhone":clientPhone}
    f.write(json.dumps(book))
    return render_template('booking_done.html', clientWeekday=clientWeekday,
                           clientTime=clientTime, clientTeacher=clientTeacher,
                           clientName=clientName, clientPhone=clientPhone)



if __name__ == '__main__':
    app.run()