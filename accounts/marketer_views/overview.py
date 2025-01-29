from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, MarketerPanelSerializer
from accounts.models import User,MarketerPanel
from accounts.views.permissions.is_marketer import IsMarketer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, filters, status, pagination, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from drf_yasg.utils import swagger_auto_schema



class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200



class MarketerOverview(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsMarketer]

    def get(self, *args, **kwargs):
        user=self.request.user
        marketer = MarketerPanel.objects.get(user=user)
        data = {
            "user": self.serializer_class(user).data,
            "marketer": MarketerPanelSerializer(marketer).data,
            "students": None,
            "payments": None,
        }
        return Response(data, status=status.HTTP_200_OK)




class Marketers(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = MarketerPanelSerializer
    queryset = MarketerPanel.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['province','city','address','occupancy_type','postal_code','description']
    ordering_fields = ['province','city','occupancy_type','id']
    filterset_fields = ['province', 'city', 'occupancy_type', 'id']
    @swagger_auto_schema()
    def get(self, request, format=None):
        query = self.filter_queryset(MarketerPanel.objects.all().order_by('id'))
        page = self.paginate_queryset(query)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
