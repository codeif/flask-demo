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
from numbers import Number
from decimal import Decimal

from flask import Blueprint

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
    """register restful api router"""
    view_func = view.as_view(endpoint)
    bp.add_url_rule(url, defaults={pk: None},
                    view_func=view_func, methods=['GET'])
    bp.add_url_rule(url, view_func=view_func, methods=['POST'])
    bp.add_url_rule('{0}<{1}:{2}>'.format(url, pk_type, pk),
                    view_func=view_func,
                    methods=['GET', 'PUT', 'DELETE', 'PATCH'])


class JSONSerializer(object):
    _json_include = None
    _json_exclude = None
    _json_simple = None

    def get_field_names(self):
        # for p in self.__mapper__.iterate_properties:
        #     yield p.key
        # _keys = self.__mapper__.c.keys()
        return [x.name for x in self.__table__.columns]

    def _get_serial_value(self, key):
        """JSON serializer for objects not serializable by default json code"""
        val = getattr(self, key)
        return self._serial_value(val)

    def _serial_value(self, val):
        if val is None or isinstance(val, (str, int)):
            pass
        elif isinstance(val, Decimal):
            return float(val)
        elif isinstance(val, Number):
            pass
        elif isinstance(val, datetime):
            val = val.isoformat(' ')
        elif isinstance(val, (date, time)):
            val = val.isoformat()
        elif isinstance(val, JSONSerializer):
            val = val.to_json_simple()
        elif isinstance(val, list):
            l = []
            for item in val:
                l.append(self._serial_value(item))
            val = l

        return val

    def _get_json_keys(self, include, exclude, only):
        if only:
            return only

        exclude_set = {'password', 'insert_time'}
        if self._json_exclude:
            exclude_set.update(self._json_exclude)
        if exclude:
            exclude_set.update(exclude)

        include_set = set()
        if self._json_include:
            include_set.update(self._json_include)
        if include:
            include_set.update(include)

        keys_set = set(self.get_field_names())
        keys_set.difference_update(exclude_set)
        keys_set.update(include_set)

        return keys_set

    def to_json(self, include=None, exclude=None, only=None):
        keys = self._get_json_keys(include, exclude, only)
        data = {key: self._get_serial_value(key) for key in keys}
        return data or None

    def to_json_simple(self):
        only = self._json_simple or [x for x in self.get_field_names() if
                                     x in ['id', 'name']]
        return self.to_json(only=only)
