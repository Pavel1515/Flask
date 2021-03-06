from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin

from packages.config import key


app = Flask(__name__)

app.secret_key = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login_all'

from packages import routes, modells

db.create_all()

