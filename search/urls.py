from django.urls import path
from search.views import TextSearch

urlpatterns = [
    path("text-search", TextSearch.as_view(), name="text-search"),
]
