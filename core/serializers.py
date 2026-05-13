from rest_framework import serializers

from core.models import ClassifiedDocument


class DocumentUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False,
        max_length=3,
    )


class ClassifiedDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedDocument
        fields = [
            "id",
            "filename",
            "category",
            "confidence",
            "created_at",
        ]


class ClassifiedDocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedDocument
        fields = [
            "id",
            "filename",
            "category",
            "confidence",
            "extracted_fields",
            "raw_text_preview",
            "model_used",
            "processing_time_ms",
            "error_message",
            "created_at",
        ]


class ClassifiedDocumentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedDocument
        fields = [
            "id",
            "filename",
            "category",
            "confidence",
            "extracted_fields",
            "raw_text_preview",
            "model_used",
            "processing_time_ms",
            "error_message",
        ]
