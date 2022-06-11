from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "12421412412"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
from sweater import models, rotes


db.create_all()