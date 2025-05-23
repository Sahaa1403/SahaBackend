from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from config.settings import STATIC_ROOT, STATIC_URL, MEDIA_URL, MEDIA_ROOT
from . import views
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Saha API",
        default_version='v1',
        description="API documentation for Saha",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@saha.ir"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', views.index, name='home'),
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/search/", include("search.urls")),
    path("api/v1/blog/", include("blog.urls")),
    path("api/v1/support/", include("support.urls")),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
