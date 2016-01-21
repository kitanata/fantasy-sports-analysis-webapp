from django.test import (
    TestCase, RequestFactory, Client, override_settings
)
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.six.moves.urllib.parse import urlsplit
from django.contrib.messages.storage.fallback import FallbackStorage

from ..forms import EmailUserCreationForm
from ..views import signup


# helper, from here:
# https://lorinstechblog.wordpress.com/2013/01/07/adding-a-session-to-a-django-request-generated-by-requestfactory/
def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()


def add_messages_to_request(request):
    """Annotate a request object with messages storage"""
    storage = FallbackStorage(request)
    request._messages = storage


class UserSignupTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_returns_200_on_get(self):
        request = self.factory.get(reverse('signup'))
        response = signup(request)
        self.assertEqual(response.status_code, 200)

    def test_populates_context_with_form(self):
        request = self.factory.get(reverse('signup'))
        response = signup(request)
        self.assertIsInstance(response.context_data['form'],
                              EmailUserCreationForm)

    def test_creates_user_on_post(self):
        data = {
            'email': 'example@example.com',
            'password1': '123456',
            'password2': '123456',
        }

        request = self.factory.post(reverse('signup'), data)
        add_session_to_request(request)
        add_messages_to_request(request)
        response = signup(request)

        user = get_user_model().objects.get(email=data['email'])
        self.assertIsNotNone(user)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(request._messages), 1)

        self.assertEqual(
            list(request._messages)[0].message,
            ('Thanks for creating an account! You can access your account '
             'details through the dropdown in the upper right of the page'
             '.')
        )

    # Regular staticfiles storage over whitenoise means we don't get a
    # ValueError due to not finding main.css (because it hasn't been built)
    @override_settings(STATICFILES_STORAGE=('django.contrib.staticfiles'
                                            '.storage.StaticFilesStorage'))
    def test_redirects_on_successful_post_and_logs_in(self):
        client = Client()

        data = {
            'email': 'example@example.com',
            'password1': '123456',
            'password2': '123456',
        }

        response = client.post(reverse('signup'), data)
        self.assertRedirects(response, reverse('dashboard'))

        # from the django source, using it to grab the next page.
        # https://github.com/django/django/blob/master/django/test/testcases.py#L292
        url = response.url
        scheme, netloc, path, query, fragment = urlsplit(url)

        next_response = client.get(path)

        self.assertTrue(
            next_response.context['request'].user.is_authenticated())
