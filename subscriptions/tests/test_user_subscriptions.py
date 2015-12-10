from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch, MagicMock
from accounts.factories import EmailUserFactory
from ..factories import ProductFactory, SubscriptionFactory
from ..models import Subscription, Product, Sport
from ..views import user_subscriptions


class UserSubscriptionsTest(TestCase):
    @patch('recurly.Plan', MagicMock(name='Plan'))
    def setUp(self):
        self.factory = RequestFactory()
        user = EmailUserFactory()
        self.request = self.factory.get(reverse('user_subscriptions'))
        self.request.user = user
        self.product = ProductFactory()
        self.subscription = SubscriptionFactory(
            user=user,
            product=self.product
        )

    def test_returns_200(self):
        response = user_subscriptions(self.request)
        self.assertEqual(response.status_code, 200)

    def test_context_populates_with_data(self):
        today = timezone.now()
        response = user_subscriptions(self.request)
        data = response.context_data['subscriptions_by_sport']

        self.assertEqual(len(data), 1)
        self.assertEqual(len(data[0]['products']), 1)
        self.assertEqual(data[0]['products'][0]['product'], self.product)
        self.assertTrue(data[0]['products'][0]['is_subscribed'])
