# coding: utf-8
from wtforms import Form
from wtforms.fields import TextField
from wtforms.validators import Regexp

from helpers import ValidatorUnique
from user.models import User


class UserForm(Form):
    name = TextField(u"нэр")
    email = TextField(u"и-мэйл")
    phone = TextField(u"утас",
                [Regexp(r"^\d{8}$", 0, u"утас оруулна уу"),
                 ValidatorUnique(User, User.phone, u"бүртгэгдсэн байна")])
    code = TextField(u"код", [Regexp(r"^\d{4}$", 0, u"оруулна уу")])
    uid = None
