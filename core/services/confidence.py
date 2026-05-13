from core.models import ClassifiedDocument
from core.services.prompt_builder import CATEGORY_FIELDS


def calculate_confidence(category, extracted_fields, raw_text):
    """
    Heuristic:
    - high: enough text and at least 70% expected fields extracted
    - medium: enough text and at least 40% expected fields extracted
    - low: weak text, unknown category, or few extracted fields
    """
    if not raw_text or len(raw_text.strip()) < 50:
        return ClassifiedDocument.Confidence.LOW

    if category not in CATEGORY_FIELDS:
        return ClassifiedDocument.Confidence.LOW

    expected_fields = CATEGORY_FIELDS.get(category, [])

    if category == "other":
        return ClassifiedDocument.Confidence.LOW

    if not expected_fields:
        return ClassifiedDocument.Confidence.LOW

    extracted_count = len(
        [
            value
            for value in extracted_fields.values()
            if value is not None and str(value).strip()
        ]
    )

    ratio = extracted_count / len(expected_fields)

    if ratio >= 0.7:
        return ClassifiedDocument.Confidence.HIGH

    if ratio >= 0.4:
        return ClassifiedDocument.Confidence.MEDIUM

    return ClassifiedDocument.Confidence.LOW
