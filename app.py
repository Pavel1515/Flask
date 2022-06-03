from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Date_b(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(300),nullable = False)
    text = db.Column(db.Text, nullable = False)
    time = db.Column(db.DateTime,default=datetime.utcnow)

    def __repl__(self):
        return '<Date_b %r>' % self.id

@app.route("/")
def index():
    base = Date_b.query.all()
    return render_template("index.html", base = base)
    

@app.route('/form', methods=['POST','GET'])
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
def dellete(id):
    base = Date_b.query.get(id)
    try:
        db.session.delete(base)     
        db.session.commit()
        return redirect('http://127.0.0.1:5000/')
    except:
        return "База даных не доступна" 


if __name__ == "__main__":
    app.run(debug=True)