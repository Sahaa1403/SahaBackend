from django.urls import path
from search.views import Search,MediaSearch,Answer
from search.mongodb import check_mongodb_connection


urlpatterns = [
    path("search", Search.as_view(), name="search"),
    path("media-search", MediaSearch.as_view(), name="media-search"),
    path("answer/<int:id>/", Answer.as_view(),name="answer"),
    path("check-mongodb-connection", check_mongodb_connection, name="check-mongodb-connection"),
]
