from kavenegar import APIException, HTTPException, KavenegarAPI
from config.settings import KAVENEGAR_API_KEY, KAVENEGAR_TEMPLATE


def send_sms_otp(phone_number: str, code: str) -> bool:
    api = KavenegarAPI(KAVENEGAR_API_KEY)
    params = {
        "receptor": phone_number,
        "template": KAVENEGAR_TEMPLATE,
        "token": code,
        "type": "sms",
    }
    try:
        api.verify_lookup(params)
        return True
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
    except Exception as e:
        print(e)
    return True


