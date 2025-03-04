from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from accounts.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class UsersList(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['created_at', 'user_type']
    search_fields = ['name', 'username', 'email']
    ordering_fields = ['created_at', 'username']

    def get(self, *args, **kwargs):
        users = self.filter_queryset(User.objects.all())
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(User.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class UserItem(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            user = User.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("User not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        try:
            user = User.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(user, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("User not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            user = User.objects.get(id=self.kwargs["id"])
            user.delete()
            return Response("User deleted.", status=status.HTTP_200_OK)
        except:
            return Response("User not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)