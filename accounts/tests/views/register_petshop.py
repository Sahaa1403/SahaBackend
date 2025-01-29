from unittest.mock import patch

import faker
from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient
from slugify import slugify

from accounts.functions import get_user_data, login
from accounts.tests.fakers import UserFactory, fake_image


class RegisterPetshopViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.client = RequestsClient()
        self.fake = faker.Faker()
        self.base_url = self.live_server_url + "/accounts/register/petshop/"
        self.user = UserFactory(
            first_name="", last_name="", user_type="petshop"
        )
        self.user.is_petshop = True
        self.user.save()
        self.token = login(self.user)[0]
        self.not_pethshop = UserFactory(user_type="normal")
        self.not_pethshop_token = login(self.not_pethshop)[0]

    def make_request(self, stage=None, data=None, files=None, token=None):
        url = self.base_url
        if stage is not None:
            url += "?stage=" + str(stage)
        headers = {}
        if token is not None:
            headers = {"ACCESS": f"Bearer {token}"}
        return self.client.patch(url, json=data, files=files, headers=headers)

    def test_401_response(self):
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_403_response(self):
        response = self.make_request(token=self.not_pethshop_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_400_response(self):
        response = self.make_request(token=self.token, stage="invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": {"stage": "invalid stage"}},
        )
        with patch("accounts.models.User.is_registered", True):
            response = self.make_request(token=self.token, stage=0)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertDictEqual(
                response.json(),
                {
                    "success": False,
                    "errors": {"stage": "user is already registered"},
                },
            )
        response = self.make_request(token=self.token, stage=-1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": {"stage": "invalid stage"}},
        )
        response = self.make_request(token=self.token, stage=4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": {"stage": "invalid stage"}},
        )
        response = self.make_request(token=self.token, stage=1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {"stage": "stage 0 is not completed"},
            },
        )

    def test_stages(self):
        # stage 0
        response = self.make_request(token=self.token, stage=0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {
                    "first_name": ["This field is required."],
                    "last_name": ["This field is required."],
                    "gender": ["This field is required."],
                    "national_id": ["This field is required."],
                },
            },
        )
        data = {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "gender": "Male",
            "national_id": self.fake.numerify("##########"),
        }
        response = self.make_request(token=self.token, stage=0, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        profile = self.user.petshop_profile
        self.assertEqual(profile.gender, data["gender"])
        self.assertEqual(profile.national_id, data["national_id"])
        self.assertEqual(response.json()["data"], {"user_data": {}})

        # stage 1
        response = self.make_request(token=self.token, stage=1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {
                    "city": ["This field is required."],
                    "postal_region": ["This field is required."],
                    "address": ["This field is required."],
                    "store_name": ["This field is required."],
                },
            },
        )
        data = {
            "city": self.fake.city(),
            "postal_region": self.fake.city(),
            "address": self.fake.address(),
            "store_name": self.fake.company(),
        }
        response = self.make_request(token=self.token, stage=1, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        shop = profile.shops
        self.assertEqual(profile.city, data["city"])
        self.assertEqual(profile.postal_region, data["postal_region"])
        self.assertEqual(profile.address, data["address"])
        self.assertEqual(shop.name, data["store_name"])
        slug = slugify(data["store_name"])
        self.assertEqual(shop.slug[: len(slug)], slug)
        self.assertEqual(response.json()["data"], {"user_data": {}})

        # stage 2
        response = self.make_request(token=self.token, stage=2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {
                    "sheba_number": ["This field is required."],
                    "estimated_item_count": ["This field is required."],
                },
            },
        )
        data = {
            "sheba_number": self.fake.numerify("IR########################"),
            "estimated_item_count": self.fake.pyint(),
        }
        response = self.make_request(token=self.token, stage=2, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.sheba_number, data["sheba_number"])
        self.assertEqual(
            profile.estimated_item_count, data["estimated_item_count"]
        )
        self.assertEqual(response.json()["data"], {"user_data": {}})

        # stage 3
        response = self.make_request(token=self.token, stage=3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {"national_card": ["This field is required."]},
            },
        )
        file = fake_image()
        files = {"national_card": file}
        response = self.make_request(token=self.token, stage=3, files=files)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertIsNotNone(profile.national_card)
        self.assertEqual(
            response.json()["data"], {"user_data": get_user_data(self.user)}
        )
