from django.db import models


class HexicProfile(models.Model):
    account = models.ForeignKey('security.Account')
    color = models.CharField(max_length=7, default="#ffffff")

class Board(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_ERROR = 0
    STATUS_IN_PROGRESS = 1

    STATUS_CHOICES = (
        (STATUS_ERROR, 'Error'),
        (STATUS_IN_PROGRESS, 'In progress'))
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)
