from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

import datetime

from ..models import LineUp, Subscription, Product
from ..views import dashboard


class SubscriptionsDashboardTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user('example@example.com')
        self.request = self.factory.get(reverse('dashboard'))
        self.request.user = self.user

        self.product1 = Product.objects.create(name='Test Product 1',
                                               duration=Product.MONTHLY)
        self.product2 = Product.objects.create(name='Test Product 2',
                                               duration=Product.MONTHLY)
        self.product3 = Product.objects.create(name='Test Product 3',
                                               duration=Product.MONTHLY)

    def test_returns_200_on_get(self):
        response = dashboard(self.request)
        self.assertEqual(response.status_code, 200)

    def test_context_is_populated_with_lineups(self):
        today = timezone.now().date()
        subscription = Subscription.objects.create(user=self.user,
                                                   product=self.product1)

        lineup = LineUp.objects.create(pdf='/tmp/notreal', date_uploaded=today)
        lineup.products.add(self.product1)
        lineup.save()

        response = dashboard(self.request)
        data = response.context_data['lineups_by_date']

        # Data structure:

        # [{
        #     'date': '<date here>',
        #     'lineups': [
        #          {lineup1}, {lineup2}
        #     ]
        # }]

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date'], today)
        self.assertEqual(len(data[0]['lineups']), 1)
        self.assertEqual(data[0]['lineups'][0], lineup)

    def test_lineups_only_appear_if_user_subscribed_prior_to_upload(self):
        today = timezone.now().date()
        three_days_ago = today - datetime.timedelta(days=3)

        subscription = Subscription.objects.create(user=self.user,
                                                   product=self.product1,
                                                   date_subscribed=today)

        lineup = LineUp.objects.create(pdf='/tmp/notreal', date_uploaded=three_days_ago)
        lineup.products.add(self.product1)
        lineup.save()

        response = dashboard(self.request)
        data = response.context_data['lineups_by_date']

        self.assertEqual(len(data), 0)

    def test_lineups_have_a_two_week_cutoff(self):
        today = timezone.now().date()
        old = today - datetime.timedelta(days=15)

        subscription = Subscription.objects.create(user=self.user,
                                                   product=self.product1)

        lineup = LineUp.objects.create(pdf='/tmp/notreal', date_uploaded=today)
        lineup.products.add(self.product1)
        lineup.save()

        old_lineup = LineUp.objects.create(pdf='/tmp/notreal', date_uploaded=old)
        old_lineup.products.add(self.product1)
        old_lineup.save()

        response = dashboard(self.request)
        data = response.context_data['lineups_by_date']

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date'], today)
        self.assertEqual(len(data[0]['lineups']), 1)
        self.assertEqual(data[0]['lineups'][0], lineup)
