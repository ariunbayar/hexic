from django import forms
from django.core.validators import RegexValidator

from board.models import Board


class BoardForm(forms.Form):
    board_name = forms.CharField(max_length=50,
                                 validators=[RegexValidator(r'^\w+$')])

    def clean(self):
        cleaned_data = super(BoardForm, self).clean()
        if 'board_name' in cleaned_data:
            qs_count = Board.objects.filter(name=cleaned_data['board_name'])
            if qs_count.count():
                msg = 'Board "%s" already exists!' % cleaned_data['board_name']
                self._errors['board_name'] = self.error_class([msg])
                del cleaned_data['board_name']

        return cleaned_data
