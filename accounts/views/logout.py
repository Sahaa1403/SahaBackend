from django.utils.translation import gettext as _
from rest_framework.views import APIView

from accounts.functions import expire
from config.responses import ok


class Logout(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch access token from cookies or headers
        access_from_cookie = request.COOKIES.get(
            "HTTP_ACCESS"
        ) or request.COOKIES.get("HTTP_AUTHORIZATION")
        access_from_header = request.META.get(
            "HTTP_ACCESS"
        ) or request.META.get("HTTP_AUTHORIZATION")
        access = access_from_cookie or access_from_header

        # Expire the access token if it exists
        if access:
            expire(access)

        # Create a response with a success message
        response = ok({"message": _("Logged out")})

        # Delete the HTTP_ACCESS cookie and set appropriate cookie attributes
        response.delete_cookie("HTTP_ACCESS")
        response.set_cookie(
            "HTTP_ACCESS",
            "",
            path="/",
            secure=True,
            httponly=True,
            samesite="None",
            max_age=0,
        )

        # Return the response to the client
        return response
