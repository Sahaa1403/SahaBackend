from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class OverView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user=self.request.user

        data = {
            "is_profile_fill": user.is_profile_fill(),
            "user": self.serializer_class(user).data
        }
        return Response(data, status=status.HTTP_200_OK)