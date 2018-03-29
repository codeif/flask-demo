# -*- coding: utf-8 -*-
"""
    demo.core
    ~~~~~~~~~~~~

    flask-demo core module

    :copyright: (c) 2016 by codeif.
    :license: MIT, see LICENSE for more details.
"""

from werkzeug.local import LocalProxy
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


logger = LocalProxy(lambda: current_app.logger)
db = SQLAlchemy()
migrate = Migrate()