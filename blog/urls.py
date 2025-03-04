from django.urls import path
from blog.views import PostView,PostItem,AllPostsView


urlpatterns = [
    path("post", PostView.as_view(), name="post"),
    path("all-posts", AllPostsView.as_view(), name="all-posts"),
    path("post-item/<str:slug>", PostItem.as_view(),name="post-item"),
]