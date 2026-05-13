ALLOWED_CATEGORIES = [
    "identity_document",
    "employment_contract",
    "payslip",
    "invoice",
    "tax_form",
    "other",
]

CATEGORY_FIELDS = {
    "identity_document": [
        "first_name",
        "last_name",
        "date_of_birth",
        "document_number",
        "expiry_date",
        "nationality",
    ],
    "invoice": [
        "issuer",
        "recipient",
        "invoice_number",
        "invoice_date",
        "total_amount",
        "currency",
    ],
    "payslip": [
        "employee_name",
        "employer",
        "period",
        "gross_salary",
        "net_salary",
        "currency",
    ],
    "employment_contract": [
        "employee_name",
        "employer",
        "start_date",
        "job_title",
        "contract_type",
    ],
    "tax_form": [
        "taxpayer_name",
        "tax_code",
        "tax_year",
        "income_amount",
        "form_type",
    ],
    "other": [],
}


def build_classification_prompt(raw_text):
    return f"""
You are a document classification and information extraction system.

Classify the document into exactly one of these categories:
{", ".join(ALLOWED_CATEGORIES)}

Expected fields by category:
{CATEGORY_FIELDS}

Rules:
1. Return only valid JSON.
2. Do not add markdown.
3. Do not invent missing fields.
4. If a field is not present, omit it.
5. Use "other" only when the document does not clearly match another category.

Return this exact JSON structure:
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
