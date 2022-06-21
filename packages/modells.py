from packages import db, UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.String)
    super_vip = db.Column(db.Boolean,default=False)


class Date_text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.Integer)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    name_user = db.Column(db.String)


class Date_b(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    name_user = db.Column(db.String)

    def __repl__(self):
        return '<Date_b %r>' % self.id

