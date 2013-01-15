from django.test import TestCase
from security.models import Account


class APITest(TestCase):
    def test_new_msj(self):
        # Check when got wrong message
        phone = 99999999
        msg = '(Wrong message)'
        url = '/api/?phone=%%2B976596&msg=%s'

        response = self.client.get(url % msg)

        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(phone_number=phone)

        # Check add new account
        msg = '(Tand %s dugaaraas 100 negj ilgeelee)' % phone
        response = self.client.get(url % msg)

        self.assertEqual(response.status_code, 302)
        acc = Account.objects.get(phone_number=phone)
        self.assertEqual(acc.credit, 100)

        # Check credit add
        response = self.client.get(url % msg)

        self.assertEqual(response.status_code, 302)
        acc = Account.objects.get(phone_number=phone)
        self.assertEqual(acc.credit, 200)
