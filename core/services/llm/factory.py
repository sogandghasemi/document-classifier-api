import os

from core.services.llm.local import OllamaLLM
from core.services.llm.remote import OpenAILLM


def get_llm_client():
    backend = os.getenv("LLM_BACKEND", "local").lower()

    if backend == "local":
        return OllamaLLM()

    if backend == "remote":
        return OpenAILLM()

    raise ValueError(
        f"Unsupported LLM_BACKEND '{backend}'. Use 'local' or 'remote'."
    )
