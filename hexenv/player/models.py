from django.db import models


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(null=True)
    design = models.IntegerField(default=10)
    bytes = models.IntegerField(default=20)
