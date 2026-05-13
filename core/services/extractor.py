from pathlib import Path

import fitz
import pytesseract
from PIL import Image

from core.services.validator import validate_uploaded_file

from core.exceptions import TextExtractionError


def extract_text_from_file(uploaded_file):
    """
    Route the uploaded file to the correct extractor based on extension.
    Supports PDF, JPEG, JPG, and PNG.
    """
    validate_uploaded_file(uploaded_file)

    extension = Path(uploaded_file.name).suffix.lower()

    try:
        if extension == ".pdf":
            return extract_text_from_pdf(uploaded_file)

        if extension in {".jpg", ".jpeg", ".png"}:
            return extract_text_from_image(uploaded_file)

        raise TextExtractionError(f"Unsupported file type: {extension}")

    except Exception as exc:
        raise TextExtractionError(
            f"Could not extract text from '{uploaded_file.name}': {exc}"
        ) from exc


def extract_text_from_pdf(uploaded_file):
    """
    Extract selectable text from PDF pages using PyMuPDF.

    PyMuPDF is fast, lightweight, and works well for text-based PDFs.
    For scanned PDFs, OCR would be needed as a future improvement.
    """
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()

    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as document:
        for page in document:
            page_text = page.get_text("text")
            if page_text:
                text_parts.append(page_text.strip())

    text = "\n\n".join(text_parts).strip()

    if not text:
        raise TextExtractionError(
            "No selectable text found in PDF. The PDF may be scanned."
        )

    return text


def extract_text_from_image(uploaded_file):
    """
    Extract text from image using Tesseract OCR.
    """
    uploaded_file.seek(0)

    image = Image.open(uploaded_file)
    image = image.convert("RGB")

    text = pytesseract.image_to_string(
        image,
        lang="eng+ita",
        config="--psm 6",
    ).strip()

    if not text:
        raise TextExtractionError("No text detected in image.")

    return text
