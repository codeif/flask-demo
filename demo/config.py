# -*- coding: utf-8 -*-
import logging


class Config(object):
    DEBUG = False
    SECRET_KEY = b'\xd4m1<w\x15\xe2?\x1e\xe3'

    # logger settings
    LGGER_LEVEL = logging.WARN  # app.debug False有效
    LOGGER_HANDLER_POLICY = 'debug'

    # Flask-SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../sqllite.db'
    SQLALCHEMY_ECHO = False

    # Celery config
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'

    # Flask-Mail config
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'you@exampl.ecom'
    MAIL_PASSWORD = 'your email password'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
