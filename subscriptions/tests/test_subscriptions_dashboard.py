from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


class SubscriptionsDashboardTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user('example@example.com')
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user

    def test_returns_200_on_get(self):
        response = signup(self.request)
        self.assertEqual(response.status_code, 200)
