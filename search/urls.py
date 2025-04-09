from django.urls import path, include
from search.views import Search, SearchByID, MediaSearch, Answer, KnowledgeBaseViewSet, LabelViewSet
from search.mongodb import check_mongodb_connection
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'labels', LabelViewSet, basename='label')
router.register(r'knowledgebase', KnowledgeBaseViewSet, basename='knowledgebase')


urlpatterns = [
    path('kb/', include(router.urls)),
    path("search", Search.as_view(), name="search"),
    path("search/<str:id>/", SearchByID.as_view(),name="search_id"),
    path("media-search", MediaSearch.as_view(), name="media-search"),
    path("answer/<int:id>/", Answer.as_view(),name="answer"),
    path("check-mongodb-connection", check_mongodb_connection, name="check-mongodb-connection"),
]