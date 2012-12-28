from django.db import models


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=120, blank=True, unique=True, null=True)
    phone = models.IntegerField(unique=True)
    code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(blank=True, null=True)
