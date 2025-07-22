from django.urls import path
from search.views import AssignDefaultTruthLabelView, CheckNewsContentView, ImportNewsContentDetailView, ImportTestNewsContentExcelView, NewsAPIView, Search, SearchByID, MediaSearch, Answer, \
    KnowledgeBaseViewSet, KnowledgeBaseItemViewSet, LabelViewSet,LabelItemViewSet,\
    SourceViewSet,SourceItemViewSet,SourceFullAPIViewSet,SocialmediaFullAPIViewSet,\
    SocialmediaItemViewSet,AddLabelViewSet, AddSourceLabelViewSet, ObjectsNumbersAPIViewSet,\
    UploadSearch, UploadSourceFile, KnowledgeBaseFullAPIViewSet, DownloadSearchData   

urlpatterns = [
    path('kb/obj-num', ObjectsNumbersAPIViewSet.as_view(), name="obj-num"),
    path('kb/sm', SocialmediaFullAPIViewSet.as_view(), name="sm"),
    path('kb/sm/<int:id>/', SocialmediaItemViewSet.as_view(), name="sm-item"),
    path('kb/sources-full', SourceFullAPIViewSet.as_view(), name="sources-full"),
    path('kb/sources', SourceViewSet.as_view(), name="sources"),
    path('kb/sources/<int:id>/', SourceItemViewSet.as_view(), name="sources-item"),
    path('kb/sources/generate-source-files/', GenerateSourceFilesView.as_view(), name='generate-source-files'),
    path('kb/add-label', AddLabelViewSet.as_view(), name="add-label"),
    path('kb/add-source-label', AddSourceLabelViewSet.as_view(), name="add-source-label"),
    path('kb/labels', LabelViewSet.as_view(), name="labels"),
    path('kb/labels/<int:id>/', LabelItemViewSet.as_view(), name="label-item"),
    path('kb/knowledgebase', KnowledgeBaseViewSet.as_view(), name="knowledgebase"),
    path('kb/knowledgebase-full', KnowledgeBaseFullAPIViewSet.as_view(), name="knowledgebase-full"),
    path('kb/knowledgebase/<int:id>/', KnowledgeBaseItemViewSet.as_view(), name="knowledgebase-item"),
    path("upload-search", UploadSearch.as_view(), name="upload-search"),
    path("upload-source", UploadSourceFile.as_view(), name="upload-source"),
    path("search", Search.as_view(), name="search"),
    path("search/<str:id>/", SearchByID.as_view(),name="search_id"),
    path("media-search", MediaSearch.as_view(), name="media-search"),
    path("answer/<int:id>/", Answer.as_view(),name="answer"),
    path("download-search-data", DownloadSearchData.as_view(), name="download-search-data"),
    path("kb/assign-truth-label", AssignDefaultTruthLabelView.as_view(), name='assign_truth_label'),
    path('news/everything', NewsAPIView.as_view(), name='news-api'),
    path('kb/process-unprocessed', UpdateUnprocessedKBView.as_view(), name='process_kb'),
    path('kb/import-test-news-content', ImportTestNewsContentExcelView.as_view(), name='import-test-news-content'),
    path('kb/check-news-content', CheckNewsContentView.as_view(), name='check-news-content'),
    path('kb/import-news-content-detail', ImportNewsContentDetailView.as_view(), name='imported-news-detail'),

    #path("check-mongodb-connection", check_mongodb_connection, name="check-mongodb-connection"),
]