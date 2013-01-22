# coding: utf-8
from admin.models import Admin
from django import forms
from security.models import Account


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


class AccountForm(forms.ModelForm):
    acc_id = forms.IntegerField(
            required=False,
            widget=forms.HiddenInput)
    class Meta:
        model = Account


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
