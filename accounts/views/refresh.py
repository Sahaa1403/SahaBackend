from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.functions import refresh as refresh_function
from config.settings import ACCESS_TTL

class Refresh(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        refresh = self.request.data.get("refresh", "")
        try:
            access, refresh = refresh_function(refresh)
        except ValueError:
            return Response(
                {"success": False, "errors": [_("refresh is invalid")]},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = Response(
            {"success": True, "data": {"refresh_token": refresh}},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            secure=True,
            max_age=ACCESS_TTL * 24 * 3600,
            httponly=True,
            samesite="None",
        )
        return response
