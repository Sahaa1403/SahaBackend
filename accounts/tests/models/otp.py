from django.core.cache import cache
from django.test import TestCase

from accounts.models import OneTimePassword
from accounts.tests.fakers.user import UserFactory


class OneTimePasswordTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.otp = OneTimePassword(self.user)

    def test_one_time_password_model(self):
        self.assertEqual(self.otp.user, self.user)
        self.assertNotEqual(self.otp.code, None)
        self.assertNotEqual(self.otp.otp_id, None)
        self.assertTrue(cache.has_key(self.user.phone_number))
        self.assertTrue(cache.has_key(self.otp.otp_id))
        self.assertTrue(
            OneTimePassword.otp_exist(phone_number=self.user.phone_number)
        )

    def test_verify_otp_method(self):
        with self.assertRaises(ValueError):
            OneTimePassword.verify_otp(
                otp_id="invalid", otp_code=self.otp.code
            )
        with self.assertRaises(ValueError):
            OneTimePassword.verify_otp(
                otp_id=self.otp.otp_id, otp_code="invalid"
            )
        self.assertEqual(
            OneTimePassword.verify_otp(
                otp_id=self.otp.otp_id, otp_code=self.otp.code
            ),
            str(self.user.id),
        )
        cache.delete(self.user.phone_number)
        cache.delete(self.otp.otp_id)
        cache.delete(self.otp.code)
        self.assertFalse(OneTimePassword.otp_exist(self.user.phone_number))
        with self.assertRaises(ValueError):
            OneTimePassword.verify_otp(
                otp_id=self.otp.otp_id, otp_code=self.otp.code
            )
