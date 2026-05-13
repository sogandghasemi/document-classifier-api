from unittest.mock import patch

import pytest

from core.exceptions import LLMServiceError
from core.services.llm.factory import get_llm_client


pytestmark = pytest.mark.django_db


@patch("core.services.llm.local.OllamaLLM.classify_and_extract")
def test_llm_unreachable(mock_llm):
    mock_llm.side_effect = LLMServiceError("Ollama unavailable")

    client = get_llm_client()

    with pytest.raises(LLMServiceError):
        client.classify_and_extract("test")
