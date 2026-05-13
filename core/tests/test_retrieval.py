import pytest
from rest_framework.test import APIClient

from core.models import ClassifiedDocument


pytestmark = pytest.mark.django_db


def test_get_existing_document():
    document = ClassifiedDocument.objects.create(
        filename="invoice.pdf",
        category="invoice",
        confidence="high",
    )

    client = APIClient()

    response = client.get(f"/api/documents/{document.id}/")

    assert response.status_code == 200
    assert response.data["filename"] == "invoice.pdf"


def test_get_non_existing_document():
    client = APIClient()

    response = client.get("/api/documents/9999/")

    assert response.status_code == 404


def test_filter_by_category():
    ClassifiedDocument.objects.create(
        filename="a.pdf",
        category="invoice",
        confidence="high",
    )

    ClassifiedDocument.objects.create(
        filename="b.pdf",
        category="payslip",
        confidence="low",
    )

    client = APIClient()

    response = client.get("/api/documents/?category=invoice")

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert len(response.data['results']) == 1
