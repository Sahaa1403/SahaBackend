from django.test import TestCase

from accounts.models import User
from accounts.selectors import get_user, user_exists
from accounts.tests.fakers import UserFactory


class TestUserSelector(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_exists(self):
        self.assertTrue(user_exists(id=self.user.id))
        self.assertFalse(user_exists(id=self.user.id + 1))

    def test_get_user(self):
        self.assertEqual(get_user(id=self.user.id), self.user)
        self.assertRaises(User.DoesNotExist, get_user, id=self.user.id + 1)
