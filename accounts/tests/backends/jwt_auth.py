from django.test import TestCase
from rest_framework.test import APIRequestFactory

from accounts.backends import JWTAuthentication
from accounts.functions import login
from accounts.tests.fakers import UserFactory


class JWTAuthenticationBackendTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.access, self.refresh = login(self.user)
        self.auth_class = JWTAuthentication()

    def test_jwt_auth_backend(self):
        def create_request(HTTP_ACCESS=None):
            return self.factory.get(
                "/examlple", data=None, HTTP_ACCESS=HTTP_ACCESS
            )

        request_fail = create_request()
        self.assertIsNone(self.auth_class.authenticate(request_fail))

        request_raise = create_request(HTTP_ACCESS="invalid")
        self.assertIsNone(self.auth_class.authenticate(request_raise))

        request_raise = create_request(HTTP_ACCESS=self.refresh)
        self.assertIsNone(self.auth_class.authenticate(request_raise))

        request_success = create_request(HTTP_ACCESS=self.access)
        self.assertEqual(
            self.auth_class.authenticate(request_success)[0], self.user
        )

        request_success = create_request(HTTP_ACCESS=f"Bearer {self.access}")
        self.assertEqual(
            self.auth_class.authenticate(request_success)[0], self.user
        )
