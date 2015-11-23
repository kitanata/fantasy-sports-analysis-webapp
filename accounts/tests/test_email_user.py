from django.test import TestCase
from ..models import EmailUser


class EmailUserTest(TestCase):
    TEST_EMAIL = 'testuser@example.com'

    def setUp(self):
        self.user = EmailUser.objects.create_user(self.TEST_EMAIL)

    def test_can_create_user(self):
        self.assertEqual(self.user.email, self.TEST_EMAIL)

    def test_created_user_is_in_database(self):
        user = EmailUser.objects.get(email=self.TEST_EMAIL)
        self.assertEqual(user.email, self.TEST_EMAIL)

    def test_is_active_is_set_by_default(self):
        self.assertTrue(self.user.is_active)

    def test_is_staff_is_set_by_default(self):
        self.assertFalse(self.user.is_staff)

    def test_is_superuser_is_set_by_default(self):
        self.assertFalse(self.user.is_superuser)
