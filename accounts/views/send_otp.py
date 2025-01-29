import re
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from accounts.functions import send_sms_otp
from accounts.models import OneTimePassword, User
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from config.settings import OTP_CODE_LENGTH, OTP_TTL
from django.core.mail import EmailMessage
import random
import uuid
from accounts.models import User

phone_number_regex = re.compile(r"^09\d{9}")


class OTPThrottle(AnonRateThrottle):
    scope = "otp"


class SendOTP(APIView):
    permission_classes = []
    # throttle_classes = [OTPThrottle]

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        if not phone_number_regex.match(phone_number):
            return Response(
                {"success": False, "errors": [_("invalid phone number")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if OneTimePassword.otp_exist(phone_number):
            return Response(
                {"success": False, "errors": [_("otp already sent")]},
                status=status.HTTP_400_BAD_REQUEST,
            )


        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
        else:
            user = User.objects.create_user(phone_number=phone_number,username=phone_number)

        otp = OneTimePassword(user)
        #print('---- OTP ----')
        #print(otp.otp_id)
        #print(otp.code)

        done = send_sms_otp(phone_number, otp.code)
        if not done:
            return Response(
                {"success": False, "errors": [_("error in sending otp")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": True,
                "data": {"otp_id": otp.otp_id},
            },
            status=status.HTTP_200_OK,
        )


class SendUpdateOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        
        if not phone_number_regex.match(phone_number):
            return Response(
                {"success": False, "errors": [_("invalid phone number")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if User.objects.filter(phone_number=phone_number).exists():
            return Response(
                {"success": False, "errors": [_("Phone number already exists")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        throttle_key = f"otp_throttle_{phone_number}"
        if cache.get(throttle_key):
            return Response(
                {"success": False, "errors": [_("Please wait before requesting another OTP.")]},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
    
        if OneTimePassword.otp_exist(phone_number):
            return Response(
                {"success": False, "errors": [_("otp already sent")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self.request.user
        otp = OneTimePassword(user)

        cache.set(otp.otp_id, {"new_phone": phone_number, "otp_code": otp.code}, timeout=OTP_TTL)
        
        cache.set(throttle_key, True, timeout=120)

        done = send_sms_otp(phone_number, otp.code)
        if not done:
            return Response(
                {"success": False, "errors": [_("error in sending otp")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "data": {"otp_id": otp.otp_id},
            },
            status=status.HTTP_200_OK,
        )


# smtp
EMAIL_OTP_EXPIRATION = 300

class SendEmailOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if not email or "@" not in email:
            return Response(
                {"success": False, "errors": [_("Invalid email address.")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"success": False, "errors": [_("Email already exists.")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cache.get(f"email_otp_sent_{email}"):
            return Response(
                {"success": False, "errors": [_("OTP already sent. Please wait before retrying.")]},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        otp_code = str(random.randint(100000, 999999))
        otp_id = str(uuid.uuid4())

        cache.set(otp_id, {"email": email, "otp_code": otp_code}, timeout=EMAIL_OTP_EXPIRATION)
        cache.set(f"email_otp_sent_{email}", True, timeout=60)

        subject = "Email Verification Code"
        message = f"Your verification code is: {otp_code}"
        recipient_list = [email]

        try:
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=None,
                to=recipient_list,
                headers={"x-liara-tag": "email-verification"},
            )
            email_message.send()
            return Response(
                {"success": True, "data": {"otp_id": otp_id}},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "errors": [_("Something went wrong.")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
