from django.test import TestCase
from unittest.mock import patch, MagicMock
from accounts.factories import EmailUserFactory
from collections import namedtuple
from django.utils import timezone
from ..factories import ProductFactory
from ..models import Subscription
from ..receivers import new_subscription_handler


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


class TestNewSubscriptionHandler(TestCase):
    def setUp(self):
        self.now = timezone.now()
        self.product = ProductFactory()
        self.user = EmailUserFactory()
        self.sender = Sender(user=self.user)
        self.plan = Plan(plan_code=self.product.recurly_plan_code)
        self.sub = Sub(
            plan=self.plan,
            state=Subscription.ACTIVE,
            uuid='test',
            activated_at=self.now,
            canceled_at=None,
            expires_at=None
        )

    def test_handler_creates_subscription(self):
        self.assertEquals(Subscription.objects.all().count(), 0)

        new_subscription_handler(self.sender, data={
            'subscription': self.sub
        })

        self.assertEquals(Subscription.objects.all().count(), 1)

        subscription = Subscription.objects.get(
            user=self.user,
            product=self.product
        )

        self.assertEquals(subscription.uuid, 'test')
        self.assertEquals(subscription.activated_at, self.now)
        self.assertEquals(subscription.state, Subscription.ACTIVE)
