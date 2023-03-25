from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Authors API",
        default_version="v1",
        description="API endpoints for the Authos API",
        contact=openapi.Contact(email="duduoli11@hotmail.com"),
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('core_apps.profiles.urls')),
]

admin.site.site_header = "Authors Haven API Admin"
admin.site.site_title = "Authors Haven API admin Portal"
admin.site.index_title = "Welcome to the Authors Havens API Portal"
