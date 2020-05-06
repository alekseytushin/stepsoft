import datetime

import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    """Создаем модель пользователя"""
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True,
                              nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=True)
    registered_on = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now())
    confirmed_on = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    confirmed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    subscribe_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    changer_blocked = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    changer_token = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def check_sub(self):
        if self.subscribe_date:
            return datetime.datetime.now() <= self.subscribe_date
        else:
            return False

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
