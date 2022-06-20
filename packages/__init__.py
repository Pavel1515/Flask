from flask import Flask, request, redirect, render_template, url_for, flash

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin


app = Flask(__name__)

app.secret_key = "12421412412"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login_all'

from packages import routes

db.create_all()
