from django.test import TestCase
from ..models import EmailUser


class EmailUserTest(TestCase):
    TEST_EMAIL = 'testuser@example.com'

    def setUp(self):
        self.user = EmailUser.objects.create_user(self.TEST_EMAIL)

    def test_can_delete_user(self):
        self.user.delete()

        with self.assertRaises(EmailUser.DoesNotExist):
            EmailUser.objects.get(email=self.TEST_EMAIL)
