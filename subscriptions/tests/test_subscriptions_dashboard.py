import datetime
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.utils import timezone
from unittest.mock import patch, MagicMock
from accounts.factories import EmailUserFactory
from ..factories import ProductFactory, SubscriptionFactory, LineUpFactory
from ..models import Product
from ..views import dashboard


class SubscriptionsDashboardTest(TestCase):
    @patch('recurly.Plan', MagicMock(name='Plan'))
    def setUp(self):
        self.factory = RequestFactory()
        self.user = EmailUserFactory()
        self.request = self.factory.get(reverse('dashboard'))
        self.request.user = self.user
        self.product = ProductFactory(duration=Product.MONTHLY)
        self.subscription = SubscriptionFactory(
            user=self.user,
            product=self.product
        )

    def test_returns_200_on_get(self):
        response = dashboard(self.request)
        self.assertEqual(response.status_code, 200)

    def test_context_is_populated_with_lineups(self):
        today = timezone.now()
        lineup = LineUpFactory(products=[self.product])
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
        # We're calling .date() here because we want to group by
        # M/D/Y, not M/D/Y:HH:MM:SS. The latter causes some weird things
        # to happen on the dashboard.
        self.assertEqual(data[0]['date'], today.date())
        self.assertEqual(len(data[0]['lineups']), 1)
        self.assertEqual(data[0]['lineups'][0], lineup)

    def test_lineups_only_appear_if_user_subscribed_prior_to_upload(self):
        today = timezone.now()
        three_days_ago = today - datetime.timedelta(days=3)
        lineup = LineUpFactory(
            products=[self.product],
            date_uploaded=three_days_ago
        )
        response = dashboard(self.request)
        data = response.context_data['lineups_by_date']
        self.assertEqual(len(data), 0)

    def test_lineups_have_a_two_week_cutoff(self):
        today = timezone.now()
        old = today - datetime.timedelta(days=15)
        lineup = LineUpFactory(products=[self.product])
        old_lineup = LineUpFactory(
            products=[self.product],
            date_uploaded=old
        )

        response = dashboard(self.request)
        data = response.context_data['lineups_by_date']

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date'], today.date())
        self.assertEqual(len(data[0]['lineups']), 1)
        self.assertEqual(data[0]['lineups'][0], lineup)
