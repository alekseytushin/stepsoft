# -*- coding: utf-8 -*-
import flask
from flask import flash, redirect
from data import db_session
from data.users import *
from itsdangerous import URLSafeTimedSerializer
import settings

confirm = flask.Blueprint('confirm', __name__, template_folder='templates')
"""
Подтверждение пользователя при переходе по ссылке указаной на почту
"""


def confirm_token(token, expiration=3600, secret_key=settings.SECRET_KEY,
                  secret_password_salt=settings.SECURITY_PASSWORD_SALT):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(
            token,
            salt=secret_password_salt,
            max_age=expiration
        )
    except:
        return False
    return email


@confirm.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            session.add(user)
            session.commit()
    except Exception as e:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect('/guide')
