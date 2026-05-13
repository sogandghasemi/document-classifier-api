from io import BytesIO
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from core.models import ClassifiedDocument


pytestmark = pytest.mark.django_db


def create_pdf_file(name="test.pdf"):
    pdf_content = b"%PDF-1.4 fake pdf content"

    return SimpleUploadedFile(
        name=name,
        content=pdf_content,
        content_type="application/pdf",
    )


@patch("core.views.classify_uploaded_file")
def test_classify_single_file(mock_classify):
    document = ClassifiedDocument.objects.create(
        filename="test.pdf",
        category="invoice",
        confidence="high",
        extracted_fields={"issuer": "ABC"},
    )

    mock_classify.return_value = document

    client = APIClient()

    response = client.post(
        "/api/documents/classify/",
        {"files": [create_pdf_file()]},
        format="multipart",
    )

    assert response.status_code == 201
    assert len(response.data["results"]) == 1


@patch("core.views.classify_uploaded_file")
def test_classify_multiple_files(mock_classify):
    document = ClassifiedDocument.objects.create(
        filename="test.pdf",
        category="invoice",
        confidence="high",
        extracted_fields={},
    )

    mock_classify.return_value = document

    client = APIClient()

    response = client.post(
        "/api/documents/classify/",
        {
            "files": [
                create_pdf_file("a.pdf"),
                create_pdf_file("b.pdf"),
            ]
        },
        format="multipart",
    )

    assert response.status_code == 201
    assert len(response.data["results"]) == 2


def test_reject_more_than_three_files():
    client = APIClient()

    response = client.post(
        "/api/documents/classify/",
        {
            "files": [
                create_pdf_file("1.pdf"),
                create_pdf_file("2.pdf"),
                create_pdf_file("3.pdf"),
                create_pdf_file("4.pdf"),
            ]
        },
        format="multipart",
    )

    assert response.status_code == 400


def test_reject_invalid_extension():
    client = APIClient()

    invalid_file = SimpleUploadedFile(
        "malware.exe",
        b"fake content",
        content_type="application/octet-stream",
    )

    response = client.post(
        "/api/documents/classify/",
        {"files": [invalid_file]},
        format="multipart",
    )

    assert response.status_code == 201

    result = response.data["results"][0]

    assert result["category"] == "other"
    assert result["confidence"] == "low"
    assert "Unsupported file extension" in result["error_message"]
