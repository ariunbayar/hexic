from django.db import models


class HexicProfile(models.Model):
    account = models.ForeignKey('security.Account')
    color = models.CharField(max_length=7, default="#ffffff")

class ActiveBoard(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
