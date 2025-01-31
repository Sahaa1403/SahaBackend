from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.functions import login
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny


class Register(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

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
                status=status.HTTP_201_CREATED,
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
