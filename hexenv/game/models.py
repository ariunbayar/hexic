from django.db import models


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    board = models.TextField()
    position = models.PositiveSmallIntegerField()
