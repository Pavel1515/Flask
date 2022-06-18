from flask import Flask, request, redirect, render_template, url_for, flash

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "12421412412"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)
manager.login_view = 'login_all'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.String)


class Date_b(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    name_user = db.Column(db.String)

    def __repl__(self):
        return '<Date_b %r>' % self.id


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    id = request.cookies.get('id')
    base = Date_b.query.all()
    user = User.query.filter(User.id == id).first()
    return render_template("index.html", base=base, user=user)


@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    try:
        if request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")
            id = request.cookies.get('id')
            user = User.query.filter(User.id == id).first()
            data_b = Date_b(title=title, text=text, name_user=user.user_name)
            db.session.add(data_b)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template('form.html')
    except:
        return "База даных не доступна"


@app.route('/delete/<int:id>')
@login_required
def dellete(id):
    base = Date_b.query.get(id)
    try:
        db.session.delete(base)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "База даных не доступна"


@app.route("/registr", methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user_name = request.form.get("user_name")
        tel = request.form.get("tel")
        if not (login and password and password2):
            flash("Введите все поля")
        elif password != password2:
            flash("Пароли не совпадают")
        else:
            try:
                hash_psw = generate_password_hash(password)
                new_user = User(login=login, password=hash_psw, user_name=user_name, tel=tel)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login_all'))
            except:
                return "Такой логин есть"
    return render_template('registr.html')


@app.route("/login", methods=['GET', 'POST'])
def login_all():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            h = redirect(url_for('index'))
            h.set_cookie('id', str(user.id))
            login_user(user)
            return h
        else:
            return 'Ошибка авторизации'
    else:

        return render_template("login.html")


@app.route("/logaut", methods=['GET', 'POST'])
@login_required
def logaut():
    logout_user()
    return redirect(url_for('login_all'))


@app.errorhandler(404)
def pageNotFount(error):
    return redirect(url_for('login_all'))


db.create_all()

if __name__=='__main__':
    app.run(debug=True)