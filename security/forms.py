# coding: utf-8
from django import forms


class AccountForm(forms.Form):
    phone_number = forms.IntegerField(
                            max_value=99999999,
                            min_value=10000000)
    pin_code = forms.IntegerField(
                            max_value=9999,
                            min_value=1000,
                            widget=forms.PasswordInput)
