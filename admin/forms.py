# coding: utf-8
from django import forms


class AdminLoginForm(forms.Form):
    user_name = forms.CharField(
            max_length=50,
            error_messages={
                'required': 'Та нэрээ оруулна уу',
                'max_length': 'Таны нэр 50-н тэмдэгтээс'\
                              'хэтрээгүй байх ёстой'})
    password = forms.CharField(
            max_length=50,
            error_messages={
                'required': 'Та нууц үгээ оруулна уу',
                'max_length': 'Таны нууц үг 50-н тэмдэгтээс'\
                              'хэтрээгүй байх ёстой'},
                widget=forms.PasswordInput)
