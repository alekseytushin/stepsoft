from flask import Blueprint, render_template, request, session, url_for
from data import db_session
from data.users import *
from mailer.mailer import send_email
from secrets import token_hex
from datetime import datetime, timedelta
import settings

changer = Blueprint('changer', __name__, template_folder='change_temps')


# change password
@changer.route('/changepassword/', methods=['GET', 'POST'])
@changer.route('/changepassword', methods=['GET', 'POST'])
def change():
    """Функция, которая отвечает за смену пароля для пользователя"""
    params = {}
    params['css'] = url_for('static', filename='css/')

    if request.method == 'POST':
        if 'email' in request.form and request.form['email']:
            session_db = db_session.create_session()
            user = session_db.query(User).filter(User.email == request.form['email']).first()
            if user:
                if user.changer_blocked != None and user.changer_blocked > datetime.now():
                    return render_template('blocked.html', **params)
                session['lp_changer_email'] = request.form['email']
                token = token_hex(4)
                user.changer_token = token
                session_db.commit()
                # Письмо
                text = 'Ваш код подтверждения:\n' + token + '\nЕсли Вы не меняли пароль, то проигнорируйте это письмо.'
                html = render_template('email_changer_confirm.html', token=token)
                send_email(user.email, 'Изменение пароля', text, html, settings.MAIL_DEFAULT_SENDER,
                           settings.MAIL_DEFAULT_PASSWORD)
                return render_template('token.html', **params)
            else:
                params['msg'] = 'Такой пользователь не зарегистрирован. Попробуйте еще раз.'
                return render_template('email.html', **params)
        elif 'token' in request.form and request.form['token']:
            try:
                session_db = db_session.create_session()
                user = session_db.query(User).filter(User.email == session['lp_changer_email']).first()
            except Exception as e:
                return render_template('email.html', **params)
            if request.form['token'] == user.changer_token:
                return render_template('password.html', **params)
            else:
                user.changer_blocked = datetime.now() + timedelta(seconds=5)
                params['msg'] = 'Вы ввели некорктный код. Попробуйте еще раз.'
                return render_template('email.html', **params)
        elif 'password' in request.form and request.form['password']:
            try:
                session_db = db_session.create_session()
                user = session_db.query(User).filter(User.email == session['lp_changer_email']).first()
            except Exception as e:
                return render_template('email.html', **params)

            if request.form['password'] == request.form['password1']:
                user.set_password(request.form['password'])
                session_db.commit()
                return render_template('success.html', **params)
            else:
                params['msg'] = 'Пароли не совпадают. Попробуйте еще раз.'
                return render_template('password.html', **params)
        else:
            return render_template('email.html', **params)
    else:
        return render_template('email.html', **params)
