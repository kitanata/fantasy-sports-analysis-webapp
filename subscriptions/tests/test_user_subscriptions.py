from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Subscription, Product, Sport
from ..views import user_subscriptions


class UserSubscriptionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user('example@example.com')
        self.request = self.factory.get(reverse('dashboard'))
        self.request.user = self.user

        self.product1 = Product.objects.create(name='Test Product 1',
                                               duration=Product.MONTHLY)
