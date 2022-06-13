from flask import render_template, request, redirect, flash, url_for 
from werkzeug.security import  check_password_hash, generate_password_hash
from sweater.models import Date_b, User
from flask_login import  login_user, logout_user, login_required

from sweater import db, app 

@app.route("/")
@login_required
def index():
    base = Date_b.query.all()
    return render_template("index.html", base = base)
    

@app.route('/form', methods=['POST','GET'])
@login_required
def form():
    try:
        if request.method == "POST":
            title =request.form.get("title")
            text = request.form.get("text")
            data_b = Date_b(title = title , text = text)
            db.session.add(data_b)
            db.session.commit()
            return redirect("http://127.0.0.1:5000/")
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
        return redirect('http://127.0.0.1:5000/')
    except:
        return "База даных не доступна" 


@app.route("/registr", methods=['GET','POST'])
def reg():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password')
        if not(login and password and password2):
            flash("Введите все поля")
        elif password!=password:
            flash("Пароли не совпадают")
        else:
            try:
                hash_psw = generate_password_hash(password2)
                new_user = User(login = login ,password =hash_psw)
                db.session.add(new_user)
                db.session.commit()
                return redirect('http://127.0.0.1:5000/login')
            except:
                return "Такой логин есть"
    return render_template('registr.html')
   




@app.route("/login", methods=['GET','POST'])
def log():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.order_by(User.login).first()

        if user and check_password_hash(user.password , password):
            login_user(user)
            return redirect('http://127.0.0.1:5000/')
        else:
            return 'Ошибка авторизации' 
    else:
        
        return render_template("login.html")


@app.route("/logaut", methods=['GET','POST'])
@login_required
def logau():
    logout_user()
    return redirect('http://127.0.0.1:5000/login')


