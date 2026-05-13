from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import ClassifiedDocumentViewSet

router = DefaultRouter()
router.register("", ClassifiedDocumentViewSet, basename="documents")

urlpatterns = [
    path("", include(router.urls)),
]
