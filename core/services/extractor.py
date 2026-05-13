from pathlib import Path

import fitz
import pytesseract
from PIL import Image, ImageFilter, ImageOps

from core.exceptions import TextExtractionError
from core.services.validator import validate_uploaded_file


def extract_text_from_file(uploaded_file):
    validate_uploaded_file(uploaded_file)

    extension = Path(uploaded_file.name).suffix.lower()

    try:
        if extension == ".pdf":
            return extract_text_from_pdf(uploaded_file)

        if extension in {".jpg", ".jpeg", ".png"}:
            return extract_text_from_image(uploaded_file)

        raise TextExtractionError(f"Unsupported file type: {extension}")

    except TextExtractionError:
        raise

    except Exception as exc:
        raise TextExtractionError(
            f"Could not extract text from '{uploaded_file.name}': {exc}"
        ) from exc


def extract_text_from_pdf(uploaded_file):
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
    uploaded_file.seek(0)

    image = Image.open(uploaded_file)
    image = preprocess_image_for_ocr(image)

    text = pytesseract.image_to_string(
        image,
        lang="eng+ita",
        config="--oem 3 --psm 6",
    ).strip()

    if not text:
        raise TextExtractionError("No text detected in image.")

    return text


def preprocess_image_for_ocr(image):
    image = image.convert("L")

    image = ImageOps.autocontrast(image)

    scale_factor = 2
    new_size = (
        image.width * scale_factor,
        image.height * scale_factor,
    )
    image = image.resize(new_size)

    image = image.filter(ImageFilter.SHARPEN)

    threshold = 180
    image = image.point(lambda pixel: 255 if pixel > threshold else 0)

    return image
