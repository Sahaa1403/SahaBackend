import json
import random
import uuid
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from config.settings import OTP_CODE_LENGTH, OTP_TTL



def generate_otp():
    random.seed(a=None, version=2)
    return "".join(random.choices("0123456789", k=OTP_CODE_LENGTH))


class OneTimePassword:
    code = None
    otp_id = None
    user = None

    def __init__(self, user):
        self.otp_id = str(uuid.uuid4())
        self.user = user
        self.code = generate_otp()
        self.__save()

    def __save(self):
        cache.set(self.otp_id, self.__gen_value(), timeout=OTP_TTL)
        cache.set(self.user.phone_number, "", timeout=OTP_TTL)

    def __gen_value(self):
        raw_code = "{}{}".format(self.otp_id, self.code)
        raw_data = {
            "user_phone": self.user.phone_number,
            "user_id": str(self.user.id),
            "hash": make_password(raw_code),
        }
        return json.dumps(raw_data)

    def verify_otp(otp_id, otp_code):
        #if not cache.has_key(otp_id):
        if otp_id not in cache:
            raise ValueError("otp is invalid. {} -- {} ".format(otp_id, otp_code))

        value = cache.get(otp_id)
        data = json.loads(value)

        if not check_password("{}{}".format(otp_id, otp_code), data.get("hash")):
            raise ValueError(f"otp is invalid. check_password: {otp_id} - {otp_code} - {data.get('hash')} - ")

        cache.delete(otp_id)
        return data.get("user_id")

    def otp_exist(phone_number):
        return cache.has_key(phone_number)