from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from search.models import SearchData
from search.serializers import SearchDataSerializer


class Search(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        data = SearchData.objects()  # Get all MongoDB documents
        serializer = SearchDataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, *args, **kwargs):
        serializer = SearchDataSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    # Get all data
    data = SearchData.objects()
    # Create a data
    data = SearchData(text="nima", email="nima@example.com")
    data.save()
"""