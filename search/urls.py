from django.urls import path, include
from search.views import Search, SearchByID, MediaSearch, Answer, \
    KnowledgeBaseViewSet, KnowledgeBaseItemViewSet, LabelViewSet,LabelItemViewSet

urlpatterns = [
    path('kb/labels', LabelViewSet.as_view(), name="labels"),
    path('kb/labels/<int:id>/', LabelItemViewSet.as_view(), name="label-item"),
    path('kb/knowledgebase', KnowledgeBaseViewSet.as_view(), name="knowledgebase"),
    path('kb/knowledgebase/<int:id>/', KnowledgeBaseItemViewSet.as_view(), name="knowledgebase-item"),
    path("search", Search.as_view(), name="search"),
    path("search/<str:id>/", SearchByID.as_view(),name="search_id"),
    path("media-search", MediaSearch.as_view(), name="media-search"),
    path("answer/<int:id>/", Answer.as_view(),name="answer"),
    #path("check-mongodb-connection", check_mongodb_connection, name="check-mongodb-connection"),
]