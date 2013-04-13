# coding: utf-8
from django import forms
from game.models import Board


class NewBoardForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=True,
        error_messages={
            'max_length': ('Талбарын нэр 50-н тэмдэгтээс'
                           'хэтрээгүй байх ёстой')})

    def clean_name(self):
        board_name = self.cleaned_data['name']
        qs = Board.objects.filter(name=board_name,
                                  status=Board.STATUS_IN_PROGRESS)
        if qs.count() > 0:
            raise forms.ValidationError('Нэр давхцсан байна')

        return board_name
