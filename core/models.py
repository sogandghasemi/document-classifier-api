from django.db import models


class ClassifiedDocument(models.Model):
    class Category(models.TextChoices):
        IDENTITY_DOCUMENT = "identity_document", "Identity Document"
        EMPLOYMENT_CONTRACT = "employment_contract", "Employment Contract"
        PAYSLIP = "payslip", "Payslip"
        INVOICE = "invoice", "Invoice"
        TAX_FORM = "tax_form", "Tax Form"
        OTHER = "other", "Other"

    class Confidence(models.TextChoices):
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    filename = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.OTHER,
    )
    confidence = models.CharField(
        max_length=20,
        choices=Confidence.choices,
        default=Confidence.LOW,
    )
    extracted_fields = models.JSONField(default=dict, blank=True)
    raw_text = models.TextField(blank=True)
    raw_text_preview = models.TextField(blank=True)
    model_used = models.CharField(max_length=100, blank=True)
    processing_time_ms = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.filename} - {self.category} - {self.confidence}"
