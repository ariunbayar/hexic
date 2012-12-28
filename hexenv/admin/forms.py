from django.forms import ModelForm, Form, CharField

from game.models import Board
from player.models import Player


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'email', 'phone', 'code']

    def clean_email(self):
        val = self.cleaned_data['email']
        if val == '':
            val = None
        return val

    def clean_last_seen_at(self):
        val = self.cleaned_data['email']
        if val == '':
            val = None
        return val


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'board', 'position']
