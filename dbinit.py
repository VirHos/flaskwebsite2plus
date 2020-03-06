from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from modules.models import db, TeachersTable, BookingTable, RequestTable
import os

if os.path.isfile('site.db'):
    os.remove("site.db")

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


f=open('teachers.json','r')
teachers=json.loads(f.read())['teachers']
f.close()


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    db.create_all()

    for t in teachers:
        teacher = TeachersTable(id=int(t['id']),
                                name=t['name'],
                                about=t['about'],
                                rating=float(t['rating']),
                                picture=t['picture'],
                                price=int(t['price']),
                                goals=str(t['goals']),
                                free=str(t['free'])
                                )
        db.session.add(teacher)

    db.session.commit()

