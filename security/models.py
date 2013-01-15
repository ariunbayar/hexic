from django.db import models


class Account(models.Model):
    phone_number = models.IntegerField()
    pin_code = models.IntegerField()
    credit = models.IntegerField()
