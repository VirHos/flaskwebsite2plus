from flask_sqlalchemy import SQLAlchemy
#import json
db = SQLAlchemy()


class TeachersTable(db.Model):
    __tablename__ = 'teacherstable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String)
    rating = db.Column(db.Float)
    picture = db.Column(db.String)
    price = db.Column(db.Integer)
    goals = db.Column(db.String)
    #goals = db.Column(JSON, default=list)
    free = db.Column(db.String)
    booking = db.relationship("BookingTable", back_populates="clientTeacher")

class BookingTable(db.Model):
    __tablename__ = 'bookingtable'
    clientid = db.Column(db.Integer, primary_key=True)
    clientWeekday = db.Column(db.String)
    clientTime = db.Column(db.String)
    clientName = db.Column(db.String)
    clientPhone = db.Column(db.String)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacherstable.id"))
    clientTeacher = db.relationship("TeachersTable")

class RequestTable(db.Model):
    __tablename__ = 'requesttable'
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    clientName = db.Column(db.String, nullable=False)
    clientPhone = db.Column(db.String, nullable=False)