# coding: utf-8
from wtforms import Form
from wtforms.fields import TextField
from wtforms.validators import Regexp


class LoginForm(Form):
    phone = TextField(u"утас", [Regexp(r"^\d{8}$", 0, u"yтсаа оруулна уу")])
    code = TextField(u"код", [Regexp(r"^\d{4}$", 0, u"оруулна уу")])
