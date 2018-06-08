from . import JSONForm
from . import StringField
from .validators import DataRequired


class LoginForm(JSONForm):
    email = StringField('Email', [DataRequired()])
