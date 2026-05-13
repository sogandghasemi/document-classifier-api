import json
import os

from openai import OpenAI

from core.services.llm.base import BaseLLM, LLMError


class OpenAILLM(BaseLLM):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "30"))

        if not self.api_key:
            raise LLMError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(api_key=self.api_key, timeout=self.timeout)

    def classify_and_extract(self, raw_text):
        prompt = self._build_prompt(raw_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You classify documents and extract structured fields. Return only JSON.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format={"type": "json_object"},
            )
        except Exception as exc:
            raise LLMError(f"OpenAI request failed: {exc}") from exc

        try:
            content = response.choices[0].message.content
            data = json.loads(content)
        except Exception as exc:
            raise LLMError(f"Invalid JSON response from OpenAI: {exc}") from exc

        data["model_used"] = self.model
        return data

    def _build_prompt(self, raw_text):
        return f"""
Classify the document into exactly one category:
identity_document, employment_contract, payslip, invoice, tax_form, other.

Extract key fields according to the detected category.

Return only valid JSON with this exact structure:
{{
  "category": "one_of_the_allowed_categories",
  "extracted_fields": {{
    "field_name": "field_value"
  }}
}}

Document text:
\"\"\"
{raw_text[:6000]}
\"\"\"
"""
