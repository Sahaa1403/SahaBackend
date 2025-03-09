from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserTypeSerializer
from rest_framework.permissions import AllowAny
from accounts.models import UserType

class UserTypes(APIView):
    serializer_class = UserTypeSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        types = UserType.objects.all()
        serializer = self.serializer_class(types,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
