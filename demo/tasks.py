"""
    demo.tasks
    ~~~~~~~~~~~~

    flask-demo tasks module

    :copyright: (c) 2016 by codeif.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

from .core import logger
from .factory import create_celery_app

celery = create_celery_app()


@celery.task
def add(x, y):
    logger.error('{} task execute add {} + {}'
                 .format(datetime.now().isoformat(' '), x, y))
    return x + y
