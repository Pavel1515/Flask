from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from packages import manager, app, db
from packages.modells import User, Date_b, Date_text

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/<int:page>")
@login_required
def index(page=1):
    id = request.cookies.get('id')
    user = User.query.filter(User.login == id).first()
    posts = db.session.query(Date_b).paginate(page,5,False)
    return render_template("index.html", posts=posts,user=user)


@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        id = request.cookies.get('id')
        user = User.query.filter(User.login == id).first()
        data_b = Date_b(title=title, text=text, name_user=user.user_name)
        db.session.add(data_b)
        db.session.commit()
        posts = db.session.query(Date_b).all()
        return redirect(url_for("index"))
    return render_template('form.html')



@app.route('/delete/<int:id>',methods=['POST','GET'])
@login_required
def dellete(id):
    base = db.session.query(Date_b).get(id)
    login = request.cookies.get('id')
    access= db.session.query(User).filter(User.login == login).first()
    if access.super_vip == True:
        db.session.query(Date_text).filter(Date_text.chat == id).delete()
        db.session.delete(base)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



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
            h.set_cookie('id', str(user.login))
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


@app.route('/admin' , methods = ['POST','GET'])
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)


@app.errorhandler(404)
def pageNotFount(error):
    return redirect(url_for('login_all'))



@app.route('/open/<int:id>', methods=['POST','GET'])
def open_viev(id):
    state = db.session.query(Date_b).filter(Date_b.id == id).first()
    chats = db.session.query(Date_text).filter(Date_text.chat == state.id)
    if request.method == "POST":
        text = request.form.get("text")
        id = request.cookies.get('id')
        user = User.query.filter(User.login == id).first()
        data_text = Date_text(chat = state.id, text=text, name_user=user.user_name)
        db.session.add(data_text)
        db.session.commit()
    return  render_template('open.html',state = state ,chats = chats)