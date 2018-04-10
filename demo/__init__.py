# -*- coding: utf-8 -*-
from flask import jsonify, request, abort
from flask_bootstrap import Bootstrap

from . import factory
from .helpers import register_blueprints
from .exceptions import CustomException, FormValidationError


def create_app(config=None):
    app = factory.create_app(config)

    Bootstrap(app)
    configure_error_handles(app)

    # register blueprints
    register_blueprints(app, __name__ + '.views')

    before_request(app)

    return app


def before_request(app):
    @app.before_request
    def request_auth():
        if request.endpoint == 'general.index':
            return

        users = {
            'username1': 'password1',
            'username2': 'password2',
        }
        auth = request.authorization
        if not auth or users.get(auth.username) != auth.password:
            abort(401)


def configure_error_handles(app):

    @app.errorhandler(401)
    def unauthorized(error):
        resp = error.get_response()
        resp.headers['WWW-Authenticate'] = 'Basic realm="Restricted Content"'
        # resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
        return resp

    @app.errorhandler(CustomException)
    def custom_exception_handler(e):
        return jsonify(errcode=e.errcode, errmsg=e.errmsg)

    @app.errorhandler(FormValidationError)
    def form_validation_error_handler(e):
        return jsonify(errcode=e.errcode, errmsg=e.errmsg, errors=e.errors)
