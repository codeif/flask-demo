# -*- coding: utf-8 -*-
"""
    demo.helpers
    ~~~~~~~~~~~~

    flask-demo helpers module

    :copyright: (c) 2016 by codeif.
    :license: MIT, see LICENSE for more details.
"""

import importlib
from datetime import datetime, date, time
import decimal
import uuid
import json

from flask import Blueprint
from sqlalchemy.types import PickleType, String

from werkzeug.utils import find_modules


def register_blueprints(app, import_path, bp_name='bp'):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param import_path: the dotted path for the package to find child modules.
    :param bp_name: Blueprint name in views.
    """
    for name in find_modules(import_path, include_packages=True):
        mod = importlib.import_module(name)
        bp = getattr(mod, bp_name, None)
        if isinstance(bp, Blueprint):
            app.register_blueprint(bp)


def register_api(bp, view, endpoint, url, pk='item_id', pk_type='int'):
    """register restful api router

    :param bp: flask.BluePrint object
    :param view: flask.views.View object
    :param endpoint: endpint
    :param url: url path, eg: /users
    :param pk: entity id variable name
    :param pk_type: http://flask.pocoo.org/docs/0.12/quickstart/#variable-rules
    """
    view_func = view.as_view(endpoint)
    bp.add_url_rule(url, defaults={pk: None},
                    view_func=view_func, methods=['GET'])
    bp.add_url_rule(url, view_func=view_func, methods=['POST'])
    bp.add_url_rule('{0}<{1}:{2}>'.format(url, pk_type, pk),
                    view_func=view_func,
                    methods=['GET', 'PUT', 'DELETE', 'PATCH'])


class DictModel(object):
    _todict_include = None
    _todict_exclude = None
    _todict_simple = None

    def get_field_names(self):
        # for p in self.__mapper__.iterate_properties:
        #     yield p.key
        # _keys = self.__mapper__.c.keys()
        return [x.name for x in self.__table__.columns]

    def _get_todict_keys(self, include=None, exclude=None, only=None):
        if only:
            return only

        exclude_set = {'password', 'insert_time'}
        if self._todict_exclude:
            exclude_set.update(self._todict_exclude)
        if exclude:
            exclude_set.update(exclude)

        include_set = set()
        if self._todict_include:
            include_set.update(self._todict_include)
        if include:
            include_set.update(include)

        keys_set = set(self.get_field_names())
        keys_set.difference_update(exclude_set)
        keys_set.update(include_set)

        return keys_set

    def todict(self, include=None, exclude=None, only=None):
        keys = self._get_todict_keys(include, exclude, only)
        data = {key: getattr(self, key) for key in keys}
        return data or None

    def todict_simple(self):
        only = self._todict_simple or [x for x in self._get_todict_keys()
                                       if x in ['id', 'name']]
        return self.to_dict(only=only)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime):
            return o.isoformat(sep=' ', timespec='seconds')
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, time):
            return o.isoformat(timespec='seconds')
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, uuid.UUID):
            return str(o)
        else:
            return super().default(o)


class JSONPickle:
    @staticmethod
    def dumps(obj, *args, **kwargs):
        return json.dumps(obj, cls=JSONEncoder)

    @staticmethod
    def loads(obj, *args, **kwargs):
        return json.loads(obj)


class JSONType(PickleType):
    impl = String(191)

    def __init__(self, pickler=JSONPickle, **kwargs):
        super().__init__(pickler=pickler, **kwargs)
