from rest_framework import mixins, viewsets

from core.models import ClassifiedDocument
from core.serializers import (
    ClassifiedDocumentDetailSerializer,
    ClassifiedDocumentListSerializer,
)


class ClassifiedDocumentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ClassifiedDocument.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ClassifiedDocumentListSerializer
        return ClassifiedDocumentDetailSerializer

    def get_queryset(self):
        queryset = ClassifiedDocument.objects.all()

        category = self.request.query_params.get("category")
        confidence = self.request.query_params.get("confidence")

        if category:
            queryset = queryset.filter(category=category)

        if confidence:
            queryset = queryset.filter(confidence=confidence)

        return queryset
