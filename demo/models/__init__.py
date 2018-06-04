from ..core import db


class BaseModel(db.Model):
    __abstract__ = True
