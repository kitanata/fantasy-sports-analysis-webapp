import recurly
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from unittest.mock import patch
from accounts.factories import EmailUserFactory
from ..views import billing_information


class BillingInfoTest(TestCase):
    VIEW_NAME = 'billing_information'

    def setUp(self):
        self.factory = RequestFactory()
        self.user = EmailUserFactory()

    @patch('recurly.Account', spec=True)
    def test_get_with_new_user(self, account_mock):
        """ Ensure that the standard get works as expected and populates the
            returned form with the information we have (first/last name).
        """
        # We need to mock the fact that Account.get() raises NotFound and
        # we use that internally to set account to None
        account_mock.get.side_effect = recurly.errors.NotFoundError('Test')

        request = self.factory.get(reverse(self.VIEW_NAME))
        request.user = self.user

        response = billing_information(request)

        account_mock.get.assert_called_with(self.user.email)

        self.assertEqual(response.status_code, 200)

        form = response.context_data['form']
        self.assertEqual(form.initial['first_name'], self.user.first_name)
        self.assertEqual(form.initial['last_name'], self.user.last_name)

    @patch('recurly.Account', spec=True)
    def test_post_with_new_user(self, account_mock):
        """ Ensure that the standard form submission process for a new user
            works as expected and creates a Account for the user and then
            billing information
        """
        # We need to mock the fact that Account.get() raises NotFound and
        # we use that internally to set account to None
        account_mock.get.side_effect = recurly.errors.NotFoundError('Test')
        request = self.factory.post(reverse(self.VIEW_NAME), {'token': 'test'})
        request.user = self.user

        # Make sure messages works properly.
        request.session = 'session'
        request._messages = FallbackStorage(request)

        response = billing_information(request)

        account_mock.get.assert_called_with(self.user.email)
        self.assertEqual(response.status_code, 200)
        account_mock.assert_called_with(account_code=self.user.email)
        account_mock().save.assert_called_with()
        self.assertTrue(account_mock().update_billing_info.called)
        self.assertEqual(len(request._messages), 1)

        self.assertEqual(
            list(request._messages)[0].message,
            'Successfully updated your billing information.'
        )
