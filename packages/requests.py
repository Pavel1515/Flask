from flask import request

class Login:
    def __init__(self):
        self.id = request.cookies.get('id')
        self.title = request.form.get('title')
        self.text = request.form.get('text')
        self.user_name =request.form.get('user_name')   
        self.login =request.form.get('login')
        self.password =request.form.get('password')
        self.password2 =request.form.get('password2')