from django.db import models


# Constants that describe actions affected by SMS to accounts
SMS_NONE = 0
SMS_NEW_ACC = 1
SMS_DEPOSIT = 2


class Sms(models.Model):
    """ Any SMS send to our app must be stored in the model. While we process
    some of the SMS we track which accounts have affected by this SMS. """
    sender = models.CharField(max_length=20)
    text = models.CharField(max_length=255)

    # Affected account by this SMS
    account = models.ForeignKey('security.Account', blank=True, null=True)

    # Action done to this account
    ACTION_CHOICES = (
        (SMS_NONE, 'None'),
        (SMS_NEW_ACC, 'New Account Created'),
        (SMS_DEPOSIT, 'Deposit Credit'),
    )
    action = models.SmallIntegerField(choices=ACTION_CHOICES)
