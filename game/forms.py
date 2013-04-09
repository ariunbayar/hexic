# coding: utf-8
from django import forms


class NewBoardForm(forms.Form):
    name = forms.CharField(
            max_length=50,
            required=False,
            error_messages={
                'max_length': 'Талбарын нэр 50-н тэмдэгтээс'\
                                    'хэтрээгүй байх ёстой'})
