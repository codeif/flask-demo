# -*- coding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import DDL, event
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from . import BaseModel
from ..core import db


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(191), unique=True)
    _password = db.Column('password', db.String(128))

    @hybrid_property
    def password(self):
        # return self._password
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self._password, password)


# UserID从1001开始
event.listen(
    User.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;")
)
