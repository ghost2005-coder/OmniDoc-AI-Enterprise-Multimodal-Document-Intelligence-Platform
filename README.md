# OmniDoc AI

Multimodal document intelligence MVP: ingestion, OCR/text extraction, retrieval, grounded Q&A, summaries, structured extraction, and knowledge-graph export.

> **Implementation note:** this repository is a runnable, educational MVP aligned to the project description in the resume. It uses demo/synthetic data by default. It does not claim production validation, trained model performance, live sensor integrations, or real-world security efficacy. Replace or extend the documented adapters with verified datasets and models before making those claims.

## Features

- PDF/text/image ingestion endpoints and text extraction (PDF text extraction; optional Tesseract OCR for images/scans).
- Chunking, sentence-transformer embeddings, Chroma vector persistence, and a TF-IDF fallback for lightweight local runs.
- Retrieval-grounded Q&A, extractive summary, schema-based field extraction, and entity-relation graph export.
- Optional LayoutLMv3 / Qwen2.5-VL integration points are isolated behind adapters; heavyweight model weights are not bundled.

## Quick start

Requirements: Python 3.11+ and pip.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
cp .env.example .env  # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

Open API docs at http://127.0.0.1:8000/docs. For the optional dashboard, in another terminal run `streamlit run dashboard.py` (install the `dashboard` extra or use `pip install streamlit requests`).

## Tests

```bash
python -m pytest
```

## Docker

```bash
docker compose up --build
```

## Repository hygiene

- Never commit `.env`, uploaded files, model weights, production logs, or customer data.
- Use synthetic or appropriately licensed data and document its provenance.
- Treat model outputs as advisory; validate before operational use.
- See `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, and `docs/ROADMAP.md`.
