from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from accounts.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

class LastSearches(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        # nothing yet
        return Response("In progress...", status=status.HTTP_200_OK)
