from annoying.fields import JSONField
from django.db import models
from datetime import datetime, timedelta
from south.modelsinspector import add_introspection_rules


class Board(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(
            default=lambda: datetime.now() + timedelta(seconds=5))

    STATUS_ERROR = 0
    STATUS_IN_PROGRESS = 1
    STATUS_WAITING = 2

    STATUS_CHOICES = (
        (STATUS_ERROR, 'Error'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_WAITING, 'Waiting'))
    status = models.PositiveIntegerField(
                    choices=STATUS_CHOICES,
                    default=STATUS_WAITING)

    players = JSONField(default=[[0],[0]])


add_introspection_rules([], ["^annoying\.fields\.JSONField"])
