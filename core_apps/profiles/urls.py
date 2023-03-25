from rest_framework_nested import routers

from django.conf.urls import url, include

from .views import ProfileViewSet

router = routers.SimpleRouter()

router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    url(r'^', include(router.urls))
]
