import json
import os

import requests

from core.services.llm.base import BaseLLM, LLMError
from core.services.prompt_builder import build_classification_prompt


class OllamaLLM(BaseLLM):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "30"))

    def classify_and_extract(self, raw_text):
        prompt = self._build_prompt(raw_text)

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMError(f"Ollama is not reachable: {exc}") from exc

        try:
            payload = response.json()
            content = payload.get("response", "")
            data = json.loads(content)
        except Exception as exc:
            raise LLMError(f"Invalid JSON response from Ollama: {exc}") from exc

        data["model_used"] = self.model
        return data

    def _build_prompt(self, raw_text):
        return build_classification_prompt(raw_text)
