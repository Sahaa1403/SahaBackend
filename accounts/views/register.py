from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.functions import login
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer


class Register(APIView):
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
        print('----------------------access-----')
        print(access)
        print('---------------------------------')
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL * 24 * 3600,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response
