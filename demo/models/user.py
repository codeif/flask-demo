# -*- coding: utf-8 -*-
from sqlalchemy import DDL, event
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin

from . import BaseModel
from ..core import db


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(191), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# UserID从1001开始
event.listen(
    User.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;")
)
