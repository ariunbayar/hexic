# coding: utf-8
from django import forms

class AccountForm(forms.Form):
    phone_number = forms.IntegerField(
                            max_value=99999999,
                            min_value=10000000,
                            error_messages={
                                'required': 'Утасны дугаар оруулна уу',
                                'invalid': 'Утасны дугаар буруу байна',
                                'max_value': 'Утасны дугаар буруу байна',
                                'min_value': 'Утасны дугаар буруу байна'})
    pin_code = forms.IntegerField(
                            max_value=9999,
                            min_value=1000,
                            error_messages={
                                'required': 'Нууц үгээ оруулна уу',
                                'invalid': 'Нууц үг буруу байна',
                                'max_value': 'Нууц үг буруу байна',
                                'min_value': 'Нууц үг буруу байна'},
                            widget=forms.PasswordInput)
