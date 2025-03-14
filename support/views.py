from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from support.serializers import TicketSerializer
from support.models import Ticket
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class TicketView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'user', 'created_date']
    search_fields = ['title', 'body', 'answer']
    ordering_fields = ['id', 'created_date']

    def get(self, *args, **kwargs):
        usr = self.request.user
        tickets = self.filter_queryset(Ticket.objects.filter(user=usr))
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Ticket.objects.filter(user=usr))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['user'] = self.request.user.id
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class AllTicketView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'user', 'created_date']
    search_fields = ['title', 'body', 'answer']
    ordering_fields = ['id', 'created_date']

    def get(self, *args, **kwargs):
        tickets = self.filter_queryset(Ticket.objects.all())
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Ticket.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)







class TicketItem(APIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Ticket not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(ticket, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("Ticket not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(id=self.kwargs["id"])
            ticket.delete()
            return Response("Ticket deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Ticket not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)