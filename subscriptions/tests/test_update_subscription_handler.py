import datetime
from django.test import TestCase
from unittest.mock import patch, MagicMock
from accounts.factories import EmailUserFactory
from collections import namedtuple
from django.utils import timezone
from ..factories import ProductFactory, SubscriptionFactory
from ..models import Subscription
from ..receivers import update_subscription_handler


Sender = namedtuple('Sender', ['user'])
Plan = namedtuple('Plan', ['plan_code'])
Sub = namedtuple('Sub', [
    'plan',
    'state',
    'uuid',
    'activated_at',
    'canceled_at',
    'expires_at'
])


class TestUpdateSubscriptionHandler(TestCase):
    @patch('recurly.Plan', MagicMock(name='Plan'))
    def setUp(self):
        self.subscription = SubscriptionFactory()
        self.sender = Sender(user=self.subscription.user)
        self.plan = Plan(plan_code=self.subscription.product.recurly_plan_code)

    def test_handler_updates_subscription(self):
        canceled_at = self.subscription.activated_at + datetime.timedelta(
            days=30
        )

        sub = Sub(
            plan=self.plan,
            uuid='TEST',
            state=Subscription.CANCELED,
            activated_at=self.subscription.activated_at,
            canceled_at=canceled_at,
            expires_at=None,
        )

        self.assertEqual(self.subscription.canceled_at, None)
        self.assertNotEqual(self.subscription.uuid, 'TEST')

        update_subscription_handler(self.sender, data={
            'subscription': sub
        })

        self.assertEqual(self.subscription.canceled_at, canceled_at)
        self.assertEqual(self.subscription.uuid, 'TEST')
