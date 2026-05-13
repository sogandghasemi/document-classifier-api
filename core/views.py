from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.exceptions import FileValidationError
from core.models import ClassifiedDocument
from core.serializers import (
    ClassifiedDocumentDetailSerializer,
    ClassifiedDocumentListSerializer,
    ClassifiedDocumentResultSerializer,
    DocumentUploadSerializer,
)
from core.services.classifier import classify_uploaded_file
from core.services.validator import validate_file_count


class ClassifiedDocumentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ClassifiedDocument.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ClassifiedDocumentListSerializer

        if self.action == "classify":
            return DocumentUploadSerializer

        return ClassifiedDocumentDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "count": queryset.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        queryset = ClassifiedDocument.objects.all()

        category = self.request.query_params.get("category")
        confidence = self.request.query_params.get("confidence")

        if category:
            queryset = queryset.filter(category=category)

        if confidence:
            queryset = queryset.filter(confidence=confidence)

        return queryset

    @action(detail=False, methods=["get"], url_path="health")
    def health(self, request):
        from django.conf import settings

        return Response(
            {
                "status": "ok",
                "service": "document-classifier-api",
                "version": "1.0.0",
                "llm_backend": settings.LLM_BACKEND,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="classify")
    def classify(self, request):
        files = request.FILES.getlist("files")

        try:
            validate_file_count(files)
        except FileValidationError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = [
            classify_uploaded_file(uploaded_file)
            for uploaded_file in files
        ]

        serializer = ClassifiedDocumentResultSerializer(results, many=True)

        return Response(
            {"results": serializer.data},
            status=status.HTTP_201_CREATED,
        )
