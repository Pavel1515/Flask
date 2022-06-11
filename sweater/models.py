from sweater import db, manager

from flask_login import UserMixin

from datetime import datetime



class Date_b(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(300),nullable = False)
    text = db.Column(db.Text, nullable = False)
    time = db.Column(db.DateTime,default=datetime.utcnow)

    def __repl__(self):
        return '<Date_b %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)
    login = db.Column(db.String(120),nullable = False, unique=True)
    password = db.Column(db.String, nullable = False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)