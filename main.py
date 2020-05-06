# -*- coding: utf-8 -*-
import csv
import datetime

import settings
from change_password.changer import changer
from confirm.confirm import confirm
from data import db_session
from data.users import *
from flask import Flask, render_template, url_for, redirect, make_response
from flask_login import LoginManager, login_user, logout_user, current_user
from forms.form import *
from itsdangerous import URLSafeTimedSerializer
from mailer.mailer import send_email

# settings
app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = settings.SECURITY_PASSWORD_SALT
app.config['MAIL_DEFAULT_SENDER'] = settings.MAIL_DEFAULT_SENDER
app.config['MAIL_DEFAULT_PASSWORD'] = settings.MAIL_DEFAULT_PASSWORD
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('./db/db_sqlite.sqlite')
app.register_blueprint(confirm)
app.register_blueprint(changer)


#
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def set_params(params):
    params['css'] = url_for('static', filename='css/')
    params['js'] = url_for('static', filename='js/')
    params['img'] = url_for('static', filename='img/')
    params['cm'] = url_for('static', filename='cm/')
    create_forms(params)


# Form validates
def create_forms(params):
    formReg = RegForm()
    params['formRegistration'] = formReg
    formAuth = LoginForm()
    params['formAuth'] = formAuth

    # Валидация формы для регистрации
    if params['formRegistration'].validate_on_submit():
        if params['formRegistration'].password1.data != params['formRegistration'].password2.data:
            params['message_reg'] = "Пароли не совпадают"
            return render_template('index.html', **params)
        session = db_session.create_session()
        if session.query(User).filter(User.email ==
                                      params['formRegistration'].email.data).first():
            params['message_reg'] = "Такой пользователь уже есть"
            return render_template('index.html', **params)
        user = User(
            name=params['formRegistration'].name.data,
            email=params['formRegistration'].email.data,
            confirmed=False,
            registered_on=datetime.datetime.now(),
        )
        user.set_password(params['formRegistration'].password1.data)
        session.add(user)
        session.commit()
        # Письмо
        token = generate_confirmation_token(user.email)
        confirm_url = settings.DEFAULT_URL + '/confirm/' + token
        text = 'Пожалуйста, подтвердите Вашу почту, перейдя по ссылке:\n' + confirm_url + '\nЕсли Вы не регитрировались, то проигнорируйте это письмо.'
        html = render_template('email_confirm.html', confirm_url=confirm_url)
        subject = "Подтверждение почты"
        send_email(user.email, subject, text, html, app.config['MAIL_DEFAULT_SENDER'],
                   app.config['MAIL_DEFAULT_PASSWORD'])
        params['message_reg_success'] = 'Вам отправленно письмо для подтверждения на почту.'
        return render_template('guide.html', **params)

    # Валидация формы для авторизации
    if params['formAuth'].validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == params['formAuth'].email.data).first()
        if user and user.check_password(params['formAuth'].password.data):
            if user.confirmed:
                login_user(user)
                return redirect("/lesson")
            else:
                params['message_log'] = "Подтвердите почту"
                return render_template('index.html', **params)
        params['message_log'] = "Неправильные email или пароль"
        return render_template('index.html', **params)


# Pages
# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    params = {}
    set_params(params)
    return render_template('index.html', **params)


# lessons page
@app.route("/lesson/<lesson_id>")
def get_lesson(lesson_id):
    params = {}
    set_params(params)
    try:
        if int(lesson_id) > 5 and not current_user.check_sub():
            return redirect('/')
        return render_template('/lessons/a&r/' + lesson_id + '/' + 'index.html',
                               **params)
    except Exception as e:
        return make_response(render_template('404.html'), 404)


@app.route("/lesson")
@app.route("/lesson/")
def lessons():
    params = {}
    set_params(params)
    # list of lessons
    with open('./templates/lessons/names.csv', mode='r', encoding='utf-8') as names:
        reader = csv.reader(names, delimiter=';')
        params['addrs'] = []
        params['names'] = []
        for row in reader:
            params['addrs'].append('/lesson/' + row[0])
            params['names'].append(row[1])

    return render_template('/lessons/lesson.html', **params)


# users profile page
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        params = {}
        set_params(params)
        return render_template('profile.html', **params)
    else:
        return redirect("/")


# guide page
@app.route('/guide')
def guide():
    params = {}
    set_params(params)
    return render_template('/guide.html', **params)


# backend
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    else:
        pass
    return redirect("/")


# Error Handlers
@app.errorhandler(404)
def not_found(e):
    params = {}
    set_params(params)
    return make_response(render_template("/404.html", **params), 404)


@app.errorhandler(500)
def not_found(e):
    params = {}
    set_params(params)
    params['error'] = str(e)
    return make_response(render_template("/500.html", **params), 500)


# server
def main():
    app.run(port=8000)


if __name__ == '__main__':
    main()
