from django.urls import path
from search.views import Search
from search.mongodb import check_mongodb_connection


urlpatterns = [
    path("search", Search.as_view(), name="search"),
    path("check-mongodb-connection", check_mongodb_connection, name="check-mongodb-connection"),
]
