class DocumentProcessingError(Exception):
    """Base error for document processing."""


class FileValidationError(DocumentProcessingError):
    """Raised when uploaded file validation fails."""


class TextExtractionError(DocumentProcessingError):
    """Raised when text extraction fails."""


class LLMServiceError(DocumentProcessingError):
    """Raised when the LLM backend is unavailable or returns invalid output."""


class InvalidLLMResponseError(DocumentProcessingError):
    """Raised when LLM output does not match the expected structure."""
