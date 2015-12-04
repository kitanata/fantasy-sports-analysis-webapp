from django.test import TestCase
from decimal import Decimal
from unittest.mock import patch, MagicMock

from ..models import Product, Sport


class TestProduct(TestCase):
    @patch('recurly.Plan', MagicMock(name='Plan'))
    def setUp(self):
        self.sport = Sport.objects.create(name='Football')
        self.product = Product.objects.create(
            name='Test Plan',
            recurly_plan_code='test-plan',
            duration=Product.MONTHLY,
            sport=self.sport,
            price=Decimal('40.00')
        )

    def test_product_is_daily_method(self):
        self.assertFalse(self.product.is_daily())

    def test_product_is_monthly_method(self):
        self.assertTrue(self.product.is_monthly())

    @patch('recurly.Plan', spec=True)
    def test_get_recurly_plan(self, mock):
        plan = self.product.get_recurly_plan()

        mock.get.assert_called_with(self.product.recurly_plan_code)

    @patch('recurly.Plan', spec=True)
    def test_recurly_overriden_model_save(self, mock):
        self.product.save()

        self.assertTrue(mock.get.called)
        self.assertEqual(mock.get.call_count, 1)
