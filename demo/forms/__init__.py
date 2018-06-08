from datetime import datetime

from flask import request
from wtforms import DateField as DateField_
from wtforms import DateTimeField as DateTimeField_
from wtforms import DecimalField, Field, Form
from wtforms import IntegerField as IntegerField_
from wtforms import PasswordField
from wtforms import SelectField as SelectField_
from wtforms import SelectMultipleField

from ..exceptions import FormValidationError

__all__ = (
    'BaseAdminItemForm',
    'BaseItemForm',
    'BooleanField',
    'DateField',
    'DateTimeField'
    'Field',
    'Form',
    'IntegerField',
    'JSONForm',
    'ListField',
    'PasswordField',
    'SelectField',
    'SelectMultipleField',
    'StringField',
    'DecimalField',
)


class JSONForm(Form):
    class Meta:
        locales = ['zh']

    def __init__(self):
        data = request.get_json()
        super().__init__(data=data)

    def resp(self):
        if self.validate():
            item = self.save()
            return item.todict()
        raise FormValidationError(self)


class BaseItemForm(JSONForm):
    def __init__(self, item):
        self.item = item
        super().__init__()


class BaseQueryForm(Form):
    def __init__(self):
        super().__init__(formdata=request.args)


class StringField(Field):
    def process_data(self, value):
        if value is None:
            self.data = value
            return
        if not isinstance(value, str):
            self.data = None
            raise ValueError('不是字符串')
        self.data = value


class IntegerField(IntegerField_):
    def process_data(self, value):
        try:
            self.data = int(value)
        except (ValueError, TypeError):
            self.data = None
            raise ValueError(self.gettext('Not a valid integer value'))


class BooleanField(Field):
    def process_data(self, value):
        self.data = bool(value)


class ListField(Field):
    def process_data(self, value):
        if not isinstance(value, list):
            self.data = None
            raise ValueError('不是有效的列表')
        self.data = value


class SelectField(SelectField_):
    def process_data(self, value):
        if value is None:
            self.data = value
        else:
            super().process_data(value)


class DateTimeField(DateTimeField_):
    def process_data(self, value):
        if not value:
            self.data = None
            return
        try:
            self.data = datetime.strptime(value, self.format)
        except ValueError:
            self.data = None
            raise ValueError(self.gettext('Not a valid datetime value'))


class DateField(DateField_):
    def process_data(self, value):
        if not value:
            self.data = None
            return
        try:
            self.data = datetime.strptime(value, self.format).date()
        except ValueError:
            self.data = None
            raise ValueError(self.gettext('Not a valid date value'))
