from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):
    """Создаем поля форм(регистрация)"""
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password1 = PasswordField(validators=[DataRequired()])
    password2 = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    """Создаем поля форм(авторизация)"""
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()