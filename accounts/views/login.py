from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from config.settings import ACCESS_TTL


class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = Response(data, status=status.HTTP_200_OK)
            response.set_cookie(
                "HTTP_ACCESS",
                f"Bearer {data['access_token']}",
                max_age=ACCESS_TTL * 24 * 3600,
                secure=True,
                httponly=True,
                samesite="None",
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)