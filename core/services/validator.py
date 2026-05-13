from pathlib import Path

from rest_framework.exceptions import ValidationError


MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_FILES_PER_REQUEST = 3

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}


def validate_file_count(files):
    if not files:
        raise ValidationError("At least one file is required.")

    if len(files) > MAX_FILES_PER_REQUEST:
        raise ValidationError(
            f"Maximum {MAX_FILES_PER_REQUEST} files are allowed per request."
        )


def validate_uploaded_file(uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower()
    content_type = getattr(uploaded_file, "content_type", "")

    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file extension '{extension}'. Allowed: PDF, JPG, JPEG, PNG."
        )

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValidationError(
            f"Unsupported content type '{content_type}'. Allowed: PDF, JPEG, PNG."
        )

    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        raise ValidationError(
            f"File '{uploaded_file.name}' exceeds the {MAX_FILE_SIZE_MB} MB limit."
        )
