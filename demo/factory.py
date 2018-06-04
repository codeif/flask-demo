# -*- coding: utf-8 -*-
"""
    demo.factory
    ~~~~~~~~~~~~

    flask-demo factory module

    :copyright: (c) 2016 by codeif.
    :license: MIT, see LICENSE for more details.
"""

import os

from celery import Celery
from flask_migrate import Migrate

from .core import db
from .helpers import CustomFlask


def create_app(config=None):
    app = CustomFlask(__name__)

    if config is None:
        config = os.environ.get('DEMO_CONFIG')
    assert config
    app.config.from_object(config)

    db.init_app(app)
    Migrate(app, db)

    return app


def create_celery_app(app=None):
    app = app or create_app()

    celery = Celery(app.import_name,
                    backend=app.config.get('CELERY_RESULT_BACKEND'),
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
