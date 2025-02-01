from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class TextSearch(APIView):
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        data = self.request.data
        return Response(data, status=status.HTTP_200_OK)