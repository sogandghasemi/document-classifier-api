from abc import ABC, abstractmethod


class LLMError(Exception):
    pass


class BaseLLM(ABC):
    @abstractmethod
    def classify_and_extract(self, raw_text):
        """
        Return a dict with:
        category, extracted_fields, model_used
        """
        raise NotImplementedError
