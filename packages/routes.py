from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from packages import manager, app, db
from packages.modells import User, Date_b, Date_text
from packages.requests import Login


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/<int:page>")
@login_required
def index(page=1):
    user = User.query.filter(User.login == Login().id).first()
    posts = db.session.query(Date_b).order_by(Date_b.id.desc()).paginate(page,5,False)
    return render_template("index.html", posts=posts,user=user)


@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    if request.method == "POST":
        user = User.query.filter(User.login == Login().id).first()
        data_b = Date_b(title=Login().title, text=Login().text, name_user=user.user_name)
        db.session.add(data_b)
        db.session.commit()
        posts = db.session.query(Date_b).all()
        return redirect(url_for("index"))
    return render_template('form.html')


@app.route('/delete/<int:id>',methods=['POST','GET'])
@login_required
def dellete(id):
    base = db.session.query(Date_b).get(id)
    access= db.session.query(User).filter(User.login == Login().id).first()
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
        if not (login and password and password2):
            flash("Введите все поля")
        elif password != password2:
            flash("Пароли не совпадают")
        else:
            try:
                hash_psw = generate_password_hash(Login().password)
                new_user = User(login=Login().login, password=hash_psw, user_name=Login().user_name, tel=Login().tel)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login_all'))
            except:
                return "Такой логин есть"
    return render_template('registr.html')


@app.route("/login", methods=['GET', 'POST'])
def login_all():
        user = User.query.filter_by(login=Login().login).first()
        if user and check_password_hash(user.password, Login().password):
            h = redirect(url_for('index'))
            h.set_cookie('id', str(user.login))
            login_user(user)
            return h
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


@app.route('/admin_add/<int:id>',methods=['POST','GET'])
def admin_add(id):
    user = db.session.query(User).filter(User.id == id).first()
    admin = db.session.query(User).filter(User.login == 'pavelerebacan@gmail.com').first()
    if request.method == "POST":
        if admin and check_password_hash(admin.password, Login().password):
            user.super_vip = True
            db.session.commit()
            return redirect('/admin')
        else:
            return 'Нету прав попросите создателя'
    return render_template('admin_add.html',user = user,admin = admin)


@app.route('/admin_delete/<int:id>',methods=['POST','GET'])
def admin_delete(id):
    user = db.session.query(User).filter(User.id == id).first()
    admin = db.session.query(User).filter(User.login == 'pavelerebacan@gmail.com').first()
    if request.method == "POST":
        if admin and check_password_hash(admin.password, Login().password):
            user.super_vip = False
            db.session.commit()
            return redirect('/admin')
        else:
            return 'Нету прав попросите создателя'
    return render_template('admin_delete.html',user = user,admin = admin)
    

@app.errorhandler(404)
def pageNotFount(error):
    return redirect(url_for('login_all'))


@app.route('/open/<int:id>', methods=['POST','GET'])
def open_viev(id):
    state = db.session.query(Date_b).filter(Date_b.id == id).first()
    chats = db.session.query(Date_text).filter(Date_text.chat == state.id).order_by(Date_text.id.desc())
    id = request.cookies.get('id')
    user = User.query.filter(User.login == id).first()
    if request.method == "POST":
        text = request.form.get("text")
        data_text = Date_text(chat = state.id, text=text, name_user=user.user_name)
        db.session.add(data_text)
        db.session.commit()
    return  render_template('open.html',user = user, state = state ,chats = chats)


@app.route('/open/delete/<int:id>')
def delete_koments(id):
    date = db.session.query(Date_text).filter(Date_text.id==id).first()
    never = date.chat
    cooki = Login().id
    date_user = db.session.query(User).filter(User.login==cooki).first()
    if date.name_user==date_user.user_name:
        db.session.delete(date)
        db.session.commit()
        return redirect(url_for('open_viev',id =never))
    else:
        return redirect(url_for('open_viev',id =never))