from django.urls import path
from blog.views import PostView,PostItem


urlpatterns = [
    path("post", PostView.as_view(), name="post"),
    path("post-item/<str:slug>/", PostItem.as_view(),name="post-item"),
]