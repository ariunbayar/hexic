from django.forms import ModelForm, ValidationError
from player.models import Player
from django.utils.translation import ugettext as _


class LoginForm(ModelForm):
    class Meta:
        model = Player
        fields = ['phone', 'code']

    def clean(self):
        data = super(LoginForm, self).clean()
        if data.get('phone') and data.get('code'):
            qs = Player.objects
            players = qs.filter(phone=data.get('phone'))
            if not players:
                raise ValidationError(_("Username and Phone is incorrect"))
            else:
                self.instance = players[0]

        return data
