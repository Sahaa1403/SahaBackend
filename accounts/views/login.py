from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User



class Login(APIView):
    permission_classes = []

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
            user = User.objects.create_user(phone_number=phone_number)

        otp = OneTimePassword(user)
        print('---- OTP ----')
        print(otp.otp_id)
        print(otp.code)
        print("-------------")

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
