from django.contrib import admin

from core.models import ClassifiedDocument


@admin.register(ClassifiedDocument)
class ClassifiedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "filename",
        "category",
        "confidence",
        "model_used",
        "processing_time_ms",
        "created_at",
    )
    list_filter = ("category", "confidence", "created_at")
    search_fields = ("filename", "raw_text")
    readonly_fields = ("created_at",)
