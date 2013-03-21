from security.models import Account
from django.test import TestCase
from django.core.urlresolvers import reverse


class SecurityTest(TestCase):
    def setUp(self):
        acc = Account(
                phone_number=99887766,
                pin_code=1234,
                credit=0)
        acc.save()

    def test_login(self):
        # When wrong phone number
        response = self.client.post(reverse('security.views.login'), {
                                    'phone_number': 99887755,
                                    'pin_code': 1234})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('game.views.board'))
        self.assertEqual(response.status_code, 302)

        # When input is correct
        response = self.client.post(reverse('security.views.login'), {
                                    'phone_number': 99887766,
                                    'pin_code': 1234})

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('game.views.board'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Logging in
        response = self.client.post(reverse('security.views.login'), {
                                    'phone_number': 99887766,
                                    'pin_code': 1234})

        #Logging out
        response = self.client.get(reverse('security.views.logout'))

        response = self.client.get(reverse('game.views.board'))
        self.assertEqual(response.status_code, 302)
