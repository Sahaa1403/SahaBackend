from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config import responses
from accounts.functions import get_user_data, login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated

class VerifyOTP(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        otp_id = self.request.data.get("otp_id", "")
        otp_code = self.request.data.get("otp_code", "")
        try:
            user_id = OneTimePassword.verify_otp(otp_id, otp_code)
        except ValueError as e:
            error_detail = str(e)
            return Response({"success": False, "errors": error_detail}, status=status.HTTP_400_BAD_REQUEST)
        user = get_user(id=user_id) # self.request.user #

        access, refresh = login(user)

        data = {
            "refresh_token": refresh,
            "access_token": access,
            "user_data": UserSerializer(user).data,
        }
        response = Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
        #print('----------------------access-----')
        #print(access)
        #print('---------------------------------')
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL * 24 * 3600,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response


class VerifyAndUpdatePhoneNumber(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        otp_id = self.request.data.get("otp_id", "")
        otp_code = self.request.data.get("otp_code", "")

        otp_data = cache.get(otp_id)
        if not otp_data:
            return Response(
                {"success": False, "errors": [_("OTP data not found")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp_data["otp_code"] != otp_code:
            return Response(
                {"success": False, "errors": [_("Invalid OTP code")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self.request.user
        user.phone_number = otp_data["new_phone"]
        user.save()

        cache.delete(otp_id)

        return Response(
            {"success": True, "data": {"message": _("Phone number updated successfully")}},
            status=status.HTTP_200_OK,
        )
        

# smtp verify
class VerifyEmailOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        otp_id = request.data.get("otp_id")
        otp_code = request.data.get("otp_code")

        if not otp_id or not otp_code:
            return Response(
                {"success": False, "errors": _("OTP ID and code are required.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_data = cache.get(otp_id)
        if not otp_data:
            return Response(
                {"success": False, "errors": _("OTP data not found or expired.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = otp_data.get("email")
        correct_otp_code = otp_data.get("otp_code")

        if otp_code != correct_otp_code:
            return Response(
                {"success": False, "errors": _("Invalid OTP code.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        user.email = email
        user.save()

        cache.delete(otp_id)

        return Response(
            {"success": True, "message": _("Email verified and updated successfully.")},
            status=status.HTTP_200_OK,
        )
