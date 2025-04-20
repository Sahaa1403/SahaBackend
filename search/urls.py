from django.urls import path
from search.views import Search, SearchByID, MediaSearch, Answer, \
    KnowledgeBaseViewSet, KnowledgeBaseItemViewSet, LabelViewSet,LabelItemViewSet,\
    SourceViewSet,SourceItemViewSet,SourceFullAPIViewSet,SocialmediaFullAPIViewSet,SocialmediaItemViewSet

urlpatterns = [
    path('kb/sm', SocialmediaFullAPIViewSet.as_view(), name="sm"),
    path('kb/sm/<int:id>/', SocialmediaItemViewSet.as_view(), name="sm-item"),
    path('kb/sources-full', SourceFullAPIViewSet.as_view(), name="sources-full"),
    path('kb/sources', SourceViewSet.as_view(), name="sources"),
    path('kb/sources/<int:id>/', SourceItemViewSet.as_view(), name="sources-item"),
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