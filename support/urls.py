from django.urls import path
from support.views import TicketView,AllTicketView,TicketItem


urlpatterns = [
    path("ticket", TicketView.as_view(), name="ticket"),
    path("all-tickets", AllTicketView.as_view(), name="all-tickets"),
    path("ticket-item/<int:id>", TicketItem.as_view(),name="ticket-item"),
]