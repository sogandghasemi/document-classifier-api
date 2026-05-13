# Document Classifier API

A Django REST API prototype for automatic document classification and key-field extraction using an LLM. Built for EU worker posting management — handles contracts, payslips, invoices, identity documents, and tax forms.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Django](https://img.shields.io/badge/Django-4.x-green) ![DRF](https://img.shields.io/badge/DRF-3.x-red)

---

## Features

- Upload up to 3 files per request (PDF, JPEG, PNG)
- PDF text extraction with PyMuPDF
- Image OCR with Tesseract and Pillow preprocessing
- Dual LLM support — local (Ollama) or remote (OpenAI-compatible) via a single env variable
- Bilingual prompt support for English and Italian documents
- Confidence scoring based on critical field fill rate
- Persists results to SQLite database
- Filterable document history by category and confidence
- Simple browser UI for testing
- Full test suite with mocked LLM

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip
- Tesseract OCR (for image files)

```bash
# macOS
brew install tesseract
brew install tesseract-lang

# Ubuntu/Debian
sudo apt install tesseract-ocr

# Check Italian and English OCR support
tesseract --list-langs
# Expected: eng, ita
```

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/document-classifier-api.git
cd document_classifier

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env             # then edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Open the browser UI at: `http://127.0.0.1:8000/`

---

## Configuration

All configuration lives in `.env`. Never commit this file.

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# --- Switch this ONE line to change LLM provider ---
LLM_BACKEND=local          # local | remote
LLM_TIMEOUT_SECONDS=30

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest

# OpenAI-compatible (remote)
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Switching Between Providers

| `LLM_BACKEND` | Backend | Requirements |
|---------------|---------|--------------|
| `local` | Ollama (local model) | Ollama running locally (see below) |
| `remote` | OpenAI-compatible API | `OPENAI_API_KEY` in `.env` |

---

## Running with Ollama (Local)

```bash
# 1. Install Ollama from https://ollama.com

# 2. Pull the model (~4.7 GB, one time only)
ollama pull llama3

# 3. Start the Ollama server (keep this terminal open)
ollama serve

# 4. Set in .env
LLM_BACKEND=local
OLLAMA_MODEL=llama3:latest

# 5. Restart Django
python manage.py runserver
```

---

## Running with Remote LLM (OpenAI)

```bash
# Set in .env
LLM_BACKEND=remote
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1
```

The remote implementation uses the OpenAI-compatible Python client and supports custom base URLs.

---

## API Reference

### Health Check

```bash
GET /api/documents/health/
```

---

### POST `/api/documents/classify/`

Upload one or more documents (max 3 per request) for classification.

**Accepted formats:** PDF, JPEG, PNG  
**Max file size:** 5 MB per file

```bash
# Single file
curl -X POST http://127.0.0.1:8000/api/documents/classify/ \
  -F "files=@payslip.pdf"

# Multiple files
curl -X POST http://127.0.0.1:8000/api/documents/classify/ \
  -F "files=@payslip.pdf" \
  -F "files=@invoice.pdf"
```

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "filename": "Payslips_organized.pdf",
      "category": "payslip",
      "confidence": "high",
      "extracted_fields": {
        "employee_name": "John Robert Smith",
        "employer": "ABC Corporation Ltd",
        "period": "Month 6",
        "gross_salary": "3750.00",
        "net_salary": "2953.71",
        "currency": "£"
      },
      "raw_text_preview": "Payslip...",
      "model_used": "llama3:latest",
      "processing_time_ms": 9288,
      "error_message": ""
    }
  ]
}
```

---

### GET `/api/documents/{id}/`

Retrieve a previously classified document by ID.

```bash
curl http://127.0.0.1:8000/api/documents/1/
```

---

### GET `/api/documents/`

List all classified documents. Supports optional filters.

```bash
# All documents
curl http://127.0.0.1:8000/api/documents/

# Filter by category
curl "http://127.0.0.1:8000/api/documents/?category=payslip"

# Filter by confidence
curl "http://127.0.0.1:8000/api/documents/?confidence=high"

# Combined filter
curl "http://127.0.0.1:8000/api/documents/?category=invoice&confidence=high"
```

**Response:**

```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "filename": "Payslips_organized.pdf",
      "category": "payslip",
      "confidence": "high",
      "created_at": "2026-05-13T10:47:09.675446+02:00"
    }
  ]
}
```

---

## Document Categories & Extracted Fields

| Category | Extracted Fields |
|----------|-----------------|
| `identity_document` | first_name, last_name, date_of_birth, document_number, document_type, expiry_date, nationality, issuing_country |
| `employment_contract` | employee_name, employer_name, job_title, start_date, contract_type, salary, work_location, contract_duration |
| `payslip` | employee_name, employer_name, employee_tax_id, period, gross_salary, net_salary, deductions, pay_date, currency |
| `invoice` | issuer_name, issuer_vat, recipient_name, recipient_vat, invoice_number, invoice_date, total_amount, currency |
| `tax_form` | taxpayer_name, taxpayer_tax_id, employer_name, tax_year, gross_income, tax_withheld, form_type |
| `other` | document_description |

---

## Confidence Score Heuristic

Confidence is scored as `high`, `medium`, or `low` based on how many **critical fields** were successfully extracted for the detected category.

**Critical fields per category:**

| Category | Critical Fields |
|----------|----------------|
| `identity_document` | first_name, last_name, document_number, expiry_date |
| `employment_contract` | employee_name, employer_name, start_date, contract_type |
| `payslip` | employee_name, employer_name, net_salary, period |
| `invoice` | issuer_name, invoice_number, total_amount, invoice_date |
| `tax_form` | taxpayer_name, taxpayer_tax_id, gross_income, tax_year |

**Scoring logic:**

```
fill_ratio = non-null critical fields / total critical fields

high   → fill_ratio >= 0.70  AND raw text length >= 100 chars
medium → fill_ratio >= 0.40  AND raw text length >= 100 chars
low    → weak text, category "other", or too few fields extracted
```

The text length check catches bad OCR results where fields appear extracted but from garbage input. If `category == "other"`, confidence is always `low` regardless of fill rate.

---

## Technical Choices

### PDF Extraction — PyMuPDF (fitz)

Chosen over pdfplumber and pdfminer because it is significantly faster on multi-page documents and has a clean Python API. pdfplumber is more accurate for tables but slower; this project prioritises speed for single-page business documents.

> **Current limitation:** scanned PDFs without selectable text are not OCR-processed automatically. Use an image upload instead.

### OCR — Tesseract + Pillow

Tesseract was chosen because it is open-source, widely used, and supports both English and Italian OCR without extra configuration. Pillow is used to preprocess images before passing them to Tesseract, improving accuracy on low-quality scans.

### LLM Strategy Pattern

All backends (`LocalLLMBackend`, `RemoteLLMBackend`) inherit from a common `BaseLLM` ABC defined in `core/services/llm/base.py`. Shared prompt logic lives on the base class so prompts stay consistent across providers. The correct backend is selected at runtime via `core/services/llm/factory.py` — switching provider requires changing one env variable, zero code changes.

```
core/services/llm/
├── base.py       ← abstract interface
├── local.py      ← Ollama implementation
├── remote.py     ← OpenAI-compatible implementation
└── factory.py    ← reads LLM_BACKEND, returns correct instance
```

---

## Project Structure

```
document_classifier/
├── config/                  # Django settings and URLs
│   ├── settings.py
│   └── urls.py
├── core/                    # Main Django app
│   ├── models.py            # ClassifiedDocument model
│   ├── views.py             # API endpoints
│   ├── serializers.py       # Request/response serialization
│   ├── urls.py
│   ├── services/
│   │   ├── llm/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   ├── remote.py
│   │   │   └── factory.py
│   │   ├── classifier.py    # Orchestration logic
│   │   ├── confidence.py    # Confidence scoring
│   │   ├── extractor.py     # PDF and image text extraction
│   │   ├── prompt_builder.py
│   │   └── validator.py
│   └── tests/
│       ├── test_classify.py
│       ├── test_retrieval.py
│       └── test_llm_mock.py
├── templates/               # Browser UI
├── .env.example
├── .gitignore
├── Makefile
├── README.md
├── manage.py
└── requirements.txt
```

---

## Error Handling

| Scenario | HTTP Status | Response |
|----------|-------------|----------|
| Invalid file format | `400` | `{"error": "Unsupported format. Allowed: PDF, JPEG, PNG"}` |
| File too large | `400` | `{"error": "File exceeds 5 MB limit"}` |
| More than 3 files | `400` | `{"error": "Maximum 3 files per request"}` |
| No files provided | `400` | `{"error": "No files provided"}` |
| Corrupted or unreadable file | `422` | `{"error": "Could not extract text from file"}` |
| LLM timeout / unavailable | `503` | `{"error": "Classification service unavailable. Please try again later."}` |
| LLM returns invalid response | `422` | `{"error": "LLM returned an invalid response"}` |
| Document ID not found | `404` | `{"error": "Document not found"}` |
| Invalid filter value | `400` | `{"error": "Invalid category value"}` |

---

## Testing

```bash
# Run all tests
pytest

# Verbose output
pytest -v
```

**Test coverage includes:**

- Single file happy path
- Multiple files (up to 3) happy path
- Invalid file format → 400
- File too large → 400
- More than 3 files → 400
- LLM unreachable — mocked, returns 503
- LLM returns invalid JSON — mocked, returns 422
- Retrieve existing result by ID → 200
- Retrieve non-existent ID → 404
- Filter by category
- Filter by confidence

---

## Makefile

```bash
make install    # install dependencies
make migrate    # run migrations
make run        # start dev server
make test       # run test suite
make check      # lint and format check
```

---

## Security Notes

- `.env` is excluded from Git via `.gitignore`
- API keys must never be committed to the repository
- `db.sqlite3` is excluded from Git
- Uploaded test files are excluded from Git
- Rotate any secrets immediately if accidentally shared

---

## Use of AI

AI tools (Claude, ChatGPT) were used during development for step-by-step planning, code structure decisions, prompt refinement and debugging.


---

## License

MIT