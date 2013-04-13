from django.db import models
from datetime import datetime, timedelta


class Board(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(
            default=lambda: datetime.now() + timedelta(seconds=5))

    STATUS_ERROR = 0
    STATUS_IN_PROGRESS = 1

    STATUS_CHOICES = (
        (STATUS_ERROR, 'Error'),
        (STATUS_IN_PROGRESS, 'In progress'))
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)

