import faker
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import PetshopProfile, UserProfile
from accounts.tests.fakers import UserFactory


class UserModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.faker = faker.Faker()

    def test_create_user(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(phone_number="")
        phone_number = self.faker.numerify("09#########")
        user = self.User.objects.create_user(phone_number=phone_number)
        self.assertFalse(user.has_usable_password())
        self.assertTrue(
            self.User.objects.filter(phone_number=phone_number).exists()
        )
        with self.assertRaises(IntegrityError):
            user = self.User.objects.create_user(phone_number=phone_number)
        new_phone_number = self.faker.numerify("09#########")
        while new_phone_number == phone_number:
            new_phone_number = self.faker.numerify("09#########")
        password = self.faker.pystr()
        user = self.User.objects.create_user(
            phone_number=new_phone_number, password=password
        )
        self.assertTrue(user.has_usable_password())
        self.assertTrue(
            self.User.objects.filter(phone_number=new_phone_number).exists()
        )
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        phone_number = self.faker.numerify("09#########")
        password = self.faker.pystr()
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                phone_number=phone_number, password=password, is_staff=False
            )
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                phone_number=phone_number,
                password=password,
                is_superuser=False,
            )
        user = self.User.objects.create_superuser(
            phone_number=phone_number, password=password
        )
        self.assertTrue(user.has_usable_password())
        self.assertTrue(
            self.User.objects.filter(
                phone_number=phone_number, is_superuser=True, is_staff=True
            ).exists()
        )
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_is_registered(self):
        user = UserFactory(first_name="", last_name="")
        self.assertFalse(user.is_registered)
        user = UserFactory(first_name="John", last_name="Doe")
        self.assertTrue(user.is_registered)

    def test_create_profile_signals(self):
        user = UserFactory(user_type="petshop")
        self.assertTrue(PetshopProfile.objects.filter(user=user).exists())
        user = UserFactory(user_type="user")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
