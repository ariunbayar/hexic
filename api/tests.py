from django.test import TestCase
from security.models import Account
from api.models import Sms


class APITest(TestCase):
    def test_message_received(self):
        # Check when got wrong message
        phone = 99999999
        msg = '(Wrong message)'
        url = '/api/?phone=%%2B976596&msg=%s'

        response = self.client.get(url % msg)

        sms = Sms.objects.get(sender='+976596')
        self.assertEqual(sms.action, Sms.NONE)
        self.assertEqual(sms.text, '(Wrong message)')
        self.assertEqual(sms.account, None)

        self.assertEqual(response.status_code, 200)

        # Check add new account
        msg = '(Tand %s dugaaraas 100 negj ilgeelee)' % phone
        response = self.client.get(url % msg)

        self.assertEqual(response.status_code, 200)
        acc = Account.objects.get(phone_number=phone)
        self.assertEqual(acc.credit, 100)

        sms = Sms.objects.get(account=acc)
        self.assertEqual(sms.action, Sms.NEW_ACC)
        self.assertEqual(sms.text, msg)
        self.assertEqual(sms.sender, '+976596')

        # Check credit add
        response = self.client.get(url % msg)

        self.assertEqual(response.status_code, 200)
        acc = Account.objects.get(phone_number=phone)
        self.assertEqual(acc.credit, 200)

        sms = Sms.objects.get(action=Sms.DEPOSIT)
        self.assertEqual(sms.text, msg)
        self.assertEqual(sms.account, acc)
        self.assertEqual(sms.sender, '+976596')
