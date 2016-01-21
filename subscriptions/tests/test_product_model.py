from django.test import TestCase
from unittest.mock import patch, MagicMock

from ..factories import ProductFactory
from ..models import Product


class TestProduct(TestCase):
    @patch('recurly.Plan', MagicMock(name='Plan'))
    def setUp(self):
        self.product = ProductFactory(duration=Product.MONTHLY)

    def test_product_is_daily_method(self):
        self.assertFalse(self.product.is_daily())

    def test_product_is_monthly_method(self):
        self.assertTrue(self.product.is_monthly())

    @patch('recurly.Plan', spec=True)
    def test_get_recurly_plan(self, mock):
        self.product.get_recurly_plan()

        mock.get.assert_called_with(self.product.recurly_plan_code)

    @patch('recurly.Plan', spec=True)
    def test_recurly_overriden_model_save(self, mock):
        self.product.save()

        self.assertTrue(mock.get.called)
        self.assertEqual(mock.get.call_count, 1)
