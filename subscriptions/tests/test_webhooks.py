from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.core.urlresolvers import reverse

from .. import signals
from ..views import push_notifications


def generate_minimal_xml(notification_name):
    """
    Return a minimal xml string to mimic POSTed data from Recurly.
    As a caveat, we don't include any actual data in this mock, since
    we're only testing the signal routing (our code), and not that Recurly
    gives us the data we need (their code), or that the data is dispatched,
    (django's code).
    """
    return '<?xml version="1.0" encoding="UTF-8"?><{0}></{0}>'.format(
        notification_name
    )


def get_boilerplate_response(notification_name):
    """
    Return a response from the webhook view, since the only thing that differs
    between the tests is the data, which only differs on the name of the
    notification.
    """
    request = RequestFactory()
    xml = generate_minimal_xml(notification_name)
    request = request.post(
        reverse('push_notifications'),
        xml,
        content_type='application/xml'
    )
    return push_notifications(request)


class TestWebhookView(TestCase):
    @patch('subscriptions.signals.new_account_notification.send',
           MagicMock(name='send'))
    def test_new_account_notification(self):
        response = get_boilerplate_response('new_account_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.new_account_notification.send.called)
        self.assertEqual(signals.new_account_notification.send.call_count, 1)

    @patch('subscriptions.signals.canceled_account_notification.send',
           MagicMock(name='send'))
    def test_canceled_account_notification(self):
        response = get_boilerplate_response('canceled_account_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.canceled_account_notification.send.called)
        self.assertEqual(
            signals.canceled_account_notification.send.call_count, 1)

    @patch('subscriptions.signals.billing_info_updated_notification.send',
           MagicMock(name='send'))
    def test_billing_info_updated_notification(self):
        response = get_boilerplate_response(
            'billing_info_updated_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.billing_info_updated_notification.send.called)
        self.assertEqual(
            signals.billing_info_updated_notification.send.call_count, 1)

    @patch('subscriptions.signals.new_subscription_notification.send',
           MagicMock(name='send'))
    def test_new_subscription_notification(self):
        response = get_boilerplate_response(
            'new_subscription_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.new_subscription_notification.send.called)
        self.assertEqual(
            signals.new_subscription_notification.send.call_count, 1)

    @patch('subscriptions.signals.updated_subscription_notification.send',
           MagicMock(name='send'))
    def test_updated_subscription_notification(self):
        response = get_boilerplate_response(
            'updated_subscription_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.updated_subscription_notification.send.called)
        self.assertEqual(
            signals.updated_subscription_notification.send.call_count, 1)

    @patch('subscriptions.signals.expired_subscription_notification.send',
           MagicMock(name='send'))
    def test_expired_subscription_notification(self):
        response = get_boilerplate_response(
            'expired_subscription_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.expired_subscription_notification.send.called)
        self.assertEqual(
            signals.expired_subscription_notification.send.call_count, 1)

    @patch('subscriptions.signals.canceled_subscription_notification.send',
           MagicMock(name='send'))
    def test_canceled_subscription_notification(self):
        response = get_boilerplate_response(
            'canceled_subscription_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.canceled_subscription_notification.send.called)
        self.assertEqual(
            signals.canceled_subscription_notification.send.call_count, 1)

    @patch('subscriptions.signals.renewed_subscription_notification.send',
           MagicMock(name='send'))
    def test_renewed_subscription_notification(self):
        response = get_boilerplate_response(
            'renewed_subscription_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.renewed_subscription_notification.send.called)
        self.assertEqual(
            signals.renewed_subscription_notification.send.call_count, 1)

    @patch('subscriptions.signals.reactivated_account_notification.send',
           MagicMock(name='send'))
    def test_reactivated_account_notification(self):
        response = get_boilerplate_response(
            'reactivated_account_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.reactivated_account_notification.send.called)
        self.assertEqual(
            signals.reactivated_account_notification.send.call_count, 1)

    @patch('subscriptions.signals.successful_payment_notification.send',
           MagicMock(name='send'))
    def test_successful_payment_notification(self):
        response = get_boilerplate_response(
            'successful_payment_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.successful_payment_notification.send.called)
        self.assertEqual(
            signals.successful_payment_notification.send.call_count, 1)

    @patch('subscriptions.signals.failed_payment_notification.send',
           MagicMock(name='send'))
    def test_failed_payment_notification(self):
        response = get_boilerplate_response(
            'failed_payment_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.failed_payment_notification.send.called)
        self.assertEqual(
            signals.failed_payment_notification.send.call_count, 1)

    @patch('subscriptions.signals.successful_refund_notification.send',
           MagicMock(name='send'))
    def test_successful_refund_notification(self):
        response = get_boilerplate_response(
            'successful_refund_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.successful_refund_notification.send.called)
        self.assertEqual(
            signals.successful_refund_notification.send.call_count, 1)

    @patch('subscriptions.signals.void_payment_notification.send',
           MagicMock(name='send'))
    def test_void_payment_notification(self):
        response = get_boilerplate_response(
            'void_payment_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.void_payment_notification.send.called)
        self.assertEqual(
            signals.void_payment_notification.send.call_count, 1)

    @patch('subscriptions.signals.closed_invoice_notification.send',
           MagicMock(name='send'))
    def test_closed_invoice_notification(self):
        response = get_boilerplate_response(
            'closed_invoice_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.closed_invoice_notification.send.called)
        self.assertEqual(
            signals.closed_invoice_notification.send.call_count, 1)

    @patch('subscriptions.signals.past_due_invoice_notification.send',
           MagicMock(name='send'))
    def test_past_due_invoice_notification(self):
        response = get_boilerplate_response(
            'past_due_invoice_notification')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(signals.past_due_invoice_notification.send.called)
        self.assertEqual(
            signals.past_due_invoice_notification.send.call_count, 1)
