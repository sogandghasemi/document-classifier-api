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
        "issuing_country",
        "document_type",
    ],
    "invoice": [
        "seller_name",
        "seller_address",
        "seller_tax_id",
        "buyer_name",
        "buyer_address",
        "buyer_tax_id",
        "invoice_number",
        "invoice_date",
        "payment_method",
        "payment_deadline",
        "net_amount",
        "vat_amount",
        "total_amount",
        "currency",
    ],
    "payslip": [
        "employee_name",
        "employee_address",
        "employer",
        "employer_address",
        "period",
        "tax_period",
        "gross_salary",
        "net_salary",
        "tax_paid",
        "social_security_contribution",
        "national_insurance_number",
        "currency",
    ],
    "employment_contract": [
        "employee_name",
        "employer",
        "start_date",
        "end_date",
        "job_title",
        "contract_type",
        "salary",
        "working_hours",
        "work_location",
    ],
    "tax_form": [
        "taxpayer_name",
        "tax_code",
        "tax_year",
        "income_amount",
        "form_type",
        "employer",
        "withholding_tax",
    ],
    "other": [],
}


CATEGORY_DEFINITIONS = {
    "identity_document": (
        "EN: passport, identity card, residence permit, driving licence. "
        "IT: passaporto, carta d'identità, permesso di soggiorno, patente."
    ),
    "employment_contract": (
        "EN: employment contract, job contract, hiring letter, employment agreement. "
        "IT: contratto di lavoro, lettera di assunzione, accordo di lavoro."
    ),
    "payslip": (
        "EN: payslip, salary slip, payroll document, wage statement. "
        "IT: busta paga, cedolino, cedolino paga, prospetto paga."
    ),
    "invoice": (
        "EN: invoice, bill, payment request, commercial invoice. "
        "IT: fattura, fattura commerciale, nota di pagamento, richiesta di pagamento."
    ),
    "tax_form": (
        "EN: tax form, tax declaration, income certificate. "
        "IT: modulo fiscale, dichiarazione fiscale, certificazione unica, CUD, CU."
    ),
    "other": (
        "EN/IT: use only when the document does not clearly match any category."
    ),
}


FIELD_SYNONYMS = {
    "invoice_number": [
        "invoice number",
        "invoice no",
        "number",
        "numero fattura",
        "n. fattura",
        "fattura n",
        "numero documento",
    ],
    "invoice_date": [
        "invoice date",
        "date of issue",
        "issue date",
        "data fattura",
        "data di emissione",
        "data documento",
    ],
    "seller_name": [
        "seller",
        "supplier",
        "issuer",
        "from",
        "venditore",
        "fornitore",
        "emittente",
        "cedente",
        "prestatore",
    ],
    "buyer_name": [
        "buyer",
        "customer",
        "recipient",
        "bill to",
        "acquirente",
        "cliente",
        "destinatario",
        "cessionario",
        "committente",
    ],
    "seller_tax_id": [
        "seller VAT ID",
        "supplier VAT",
        "tax id",
        "partita iva venditore",
        "p.iva venditore",
        "codice fiscale venditore",
        "partita iva fornitore",
    ],
    "buyer_tax_id": [
        "buyer VAT ID",
        "customer VAT",
        "partita iva cliente",
        "p.iva cliente",
        "codice fiscale cliente",
        "partita iva acquirente",
    ],
    "total_amount": [
        "total",
        "amount due",
        "payment amount",
        "totale",
        "totale fattura",
        "importo totale",
        "totale da pagare",
    ],
    "net_amount": [
        "net amount",
        "taxable amount",
        "subtotal",
        "imponibile",
        "importo netto",
        "totale imponibile",
    ],
    "vat_amount": [
        "VAT",
        "VAT amount",
        "IVA",
        "imposta",
        "importo IVA",
    ],
    "payment_method": [
        "payment method",
        "method of payment",
        "modalità di pagamento",
        "metodo di pagamento",
    ],
    "payment_deadline": [
        "payment deadline",
        "due date",
        "scadenza pagamento",
        "data scadenza",
    ],
    "employee_name": [
        "employee",
        "worker",
        "name",
        "dipendente",
        "lavoratore",
        "nome dipendente",
    ],
    "employer": [
        "employer",
        "company",
        "datore di lavoro",
        "azienda",
        "società",
    ],
    "gross_salary": [
        "gross salary",
        "gross pay",
        "retribuzione lorda",
        "lordo",
        "totale lordo",
    ],
    "net_salary": [
        "net salary",
        "net pay",
        "take home pay",
        "retribuzione netta",
        "netto",
        "netto in busta",
    ],
    "tax_code": [
        "tax code",
        "fiscal code",
        "codice fiscale",
        "CF",
    ],
    "date_of_birth": [
        "date of birth",
        "birth date",
        "data di nascita",
        "nato il",
        "nata il",
    ],
    "document_number": [
        "document number",
        "ID number",
        "passport number",
        "numero documento",
        "numero carta",
        "numero passaporto",
    ],
    "expiry_date": [
        "expiry date",
        "expiration date",
        "valid until",
        "data di scadenza",
        "scade il",
        "valido fino al",
    ],
}


def build_classification_prompt(raw_text):
    return f"""
You are an expert bilingual document classification and information extraction system.
You work with English and Italian documents.

The OCR text may contain errors, broken lines, misspellings, mixed languages, and merged columns.
Your task is to infer the most likely structured information from the text, but never invent values that are not supported by the text.

Classify the document into exactly one of these categories:
{", ".join(ALLOWED_CATEGORIES)}

Category definitions, English and Italian:
{CATEGORY_DEFINITIONS}

Expected output fields by category:
{CATEGORY_FIELDS}

Useful field synonyms, English and Italian:
{FIELD_SYNONYMS}

General rules:
1. Return only valid JSON.
2. Do not use markdown.
3. Do not add explanations.
4. Always use the standardized English field names listed in Expected output fields.
5. Use null for fields that are missing or unclear.
6. Do not invent values.
7. Preserve original dates, names, tax codes, invoice numbers, and amounts as written when possible.
8. Preserve original currency symbols or codes, for example EUR, €, GBP, £, USD.
9. If the document is Italian, still return the field names in English.
10. If the document is English, still return the same standardized English field names.

Invoice/Fattura-specific rules:
1. seller_name must come from SELLER, supplier, issuer, cedente/prestatore, venditore, or fornitore section.
2. buyer_name must come from BUYER, customer, recipient, cessionario/committente, cliente, or acquirente section.
3. Do not merge seller and buyer into one field.
4. invoice_number is usually near Invoice, Invoice No, Number, Fattura, N. fattura, Numero fattura.
5. invoice_date is usually near Date of issue, Data fattura, Data di emissione, Data documento.
6. total_amount is the final payable amount, usually near Total, Amount due, Totale, Totale fattura, Totale da pagare.
7. net_amount is the amount before VAT/IVA.
8. vat_amount is the tax amount, usually near VAT, IVA, Imposta.

Payslip/Busta paga-specific rules:
1. employee_name is the worker/dipendente/lavoratore.
2. employer is the company/datore di lavoro/azienda.
3. gross_salary is lordo/retribuzione lorda/gross pay.
4. net_salary is netto/netto in busta/net pay.
5. period may appear as month, pay period, periodo, mese, competenza.

Identity document-specific rules:
1. first_name and last_name may appear as given name/surname or nome/cognome.
2. document_number may appear as numero documento, document no, passport no.
3. expiry_date may appear as scadenza, valido fino al, date of expiry.

Return this exact JSON structure:
{{
  "category": "one_of_the_allowed_categories",
  "extracted_fields": {{
    "field_name": "field_value_or_null"
  }}
}}

Document text:
\"\"\"
{raw_text[:8000]}
\"\"\"
"""
