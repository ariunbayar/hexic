from django import forms
from player.models import Player
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    phone = forms.IntegerField()
    object = None

    def clean(self):
        data = super(LoginForm, self).clean()
        if data.get('username') and data.get('phone'):
            qs = Player.objects
            players = qs.filter(username=data.get('username'),
                                phone=data.get('phone'))
            if not players:
                raise forms.ValidationError(_("Username and Phone is incorrect"))
            else:
                self.object = players[0]
        return data
