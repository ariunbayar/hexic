from django.db import models


class Sms(models.Model):
    """ Any SMS send to our app must be stored in the model. While we process
    some of the SMS we track which accounts have affected by this SMS. """
    sender = models.CharField(max_length=20)
    text = models.CharField(max_length=255)

    # Affected account by this SMS
    account = models.ForeignKey('security.Account', blank=True, null=True)

    # Constants that describe actions affected by SMS to accounts
    NONE = 0
    NEW_ACC = 1
    DEPOSIT = 2

    # Action done to this account
    ACTION_CHOICES = (
        (NONE, 'None'),
        (NEW_ACC, 'New Account Created'),
        (DEPOSIT, 'Deposit Credit'),
    )
    action = models.SmallIntegerField(choices=ACTION_CHOICES, default=NONE)
    date_time = models.DateTimeField(auto_now_add=True)
