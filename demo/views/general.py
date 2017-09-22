# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.views import MethodView

from ..exceptions import NoError, LoginRequired, FormValidationError

from ..forms.login import LoginForm
from ..tasks import add


bp = Blueprint('general', __name__)


class IndexView(MethodView):
    def get(self):
        raise NoError()


class ErrorView(MethodView):
    def get(self):
        raise LoginRequired()


class FormErrorView(MethodView):
    def get(self):
        form = LoginForm()
        if not form.validate():
            raise FormValidationError(form)
        raise NoError()


class CeleryTestView(MethodView):
    def get(self):
        add.delay(1, 3)
        return 'ok'


class BootstrapView(MethodView):
    def get(self):
        return render_template('bootstrap.html')


bp.add_url_rule('/', view_func=IndexView.as_view('index'))
bp.add_url_rule('/error', view_func=ErrorView.as_view('error'))
bp.add_url_rule('/form-error', view_func=FormErrorView.as_view('form_error'))
bp.add_url_rule('/celery-test',
                view_func=CeleryTestView.as_view('celery_test'))
bp.add_url_rule('/bootstrap', view_func=BootstrapView.as_view('bootstrap'))
