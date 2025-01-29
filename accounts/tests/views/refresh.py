from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from accounts.functions import login
from accounts.tests.fakers import UserFactory


class RefreshViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        user = UserFactory()
        _, self.refresh = login(user)

    def make_request(self, refresh):
        return self.rc.post(
            f"{self.live_server_url}/accounts/refresh/",
            json={"refresh": refresh},
        )

    def test_400_response(self):
        response = self.make_request("invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": ["refresh is invalid"]},
        )

    def test_200_response(self):
        response = self.make_request(self.refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get("success"))
        self.assertIn("refresh_token", response.json().get("data"))
        self.assertIn("HTTP_ACCESS", response.cookies)
