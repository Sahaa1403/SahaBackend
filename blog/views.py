from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.serializers import PostSerializer
from blog.models import Post,PostComment
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class PostView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_date', 'status', 'author', 'feedback_status', 'comment_status']
    search_fields = ['title', 'body', 'slug']
    ordering_fields = ['post_date', 'status', 'author']

    def get(self, *args, **kwargs):
        posts = self.filter_queryset(Post.objects.all())
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Post.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data['author'] = self.request.user.id
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class PostItem(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            post = Post.objects.get(slug=self.kwargs["slug"])
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Post not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        try:
            post = Post.objects.get(slug=self.kwargs["slug"])
            serializer = self.serializer_class(post, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("Post not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            post = Post.objects.get(slug=self.kwargs["slug"])
            post.delete()
            return Response("Post deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Post not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
