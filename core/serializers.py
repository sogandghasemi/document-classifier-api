from rest_framework import serializers

from core.models import ClassifiedDocument


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
