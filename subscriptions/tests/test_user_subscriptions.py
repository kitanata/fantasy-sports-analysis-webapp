from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Subscription, Product, Sport
from ..views import user_subscriptions


class UserSubscriptionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = get_user_model().objects.create_user('example@example.com')
        self.request = self.factory.get(reverse('user_subscriptions'))
        self.request.user = user

        sport = Sport.objects.create(name='Football')

        self.product = Product.objects.create(
            name='Test Product 1',
            duration=Product.MONTHLY,
            sport=sport
        )

    def test_returns_200(self):
        response = user_subscriptions(self.request)
        self.assertEqual(response.status_code, 200)

    def test_context_populates_with_data(self):
        pass
