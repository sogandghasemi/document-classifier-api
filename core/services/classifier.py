import time

from core.exceptions import (
    DocumentProcessingError,
    InvalidLLMResponseError,
)
from core.models import ClassifiedDocument
from core.services.confidence import calculate_confidence
from core.services.extractor import extract_text_from_file
from core.services.llm.factory import get_llm_client
from core.services.prompt_builder import ALLOWED_CATEGORIES


RAW_TEXT_PREVIEW_LENGTH = 500


def classify_uploaded_file(uploaded_file):
    start_time = time.perf_counter()

    try:
        raw_text = extract_text_from_file(uploaded_file)

        llm_client = get_llm_client()
        llm_result = llm_client.classify_and_extract(raw_text)

        category = _validate_category(llm_result.get("category"))
        extracted_fields = _validate_extracted_fields(
            llm_result.get("extracted_fields")
        )
        model_used = llm_result.get("model_used", "")

        confidence = calculate_confidence(
            category=category,
            extracted_fields=extracted_fields,
            raw_text=raw_text,
        )

        processing_time_ms = _elapsed_ms(start_time)

        return ClassifiedDocument.objects.create(
            filename=uploaded_file.name,
            category=category,
            confidence=confidence,
            extracted_fields=extracted_fields,
            raw_text=raw_text,
            raw_text_preview=raw_text[:RAW_TEXT_PREVIEW_LENGTH],
            model_used=model_used,
            processing_time_ms=processing_time_ms,
        )

    except DocumentProcessingError as exc:
        processing_time_ms = _elapsed_ms(start_time)

        return ClassifiedDocument.objects.create(
            filename=getattr(uploaded_file, "name", "unknown"),
            category=ClassifiedDocument.Category.OTHER,
            confidence=ClassifiedDocument.Confidence.LOW,
            extracted_fields={},
            raw_text="",
            raw_text_preview="",
            model_used="",
            processing_time_ms=processing_time_ms,
            error_message=str(exc),
        )


def _validate_category(category):
    if category not in ALLOWED_CATEGORIES:
        raise InvalidLLMResponseError(
            f"LLM returned unsupported category: {category}"
        )

    return category


def _validate_extracted_fields(extracted_fields):
    if extracted_fields is None:
        return {}

    if not isinstance(extracted_fields, dict):
        raise InvalidLLMResponseError(
            "LLM returned extracted_fields in an invalid format."
        )

    return extracted_fields


def _elapsed_ms(start_time):
    return int((time.perf_counter() - start_time) * 1000)
