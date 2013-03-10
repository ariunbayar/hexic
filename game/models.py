from django.db import models


class HexicProfile(models.Model):
    account = models.ForeignKey('security.Account')
    color = models.CharField(max_length=7, default="#ffffff")
