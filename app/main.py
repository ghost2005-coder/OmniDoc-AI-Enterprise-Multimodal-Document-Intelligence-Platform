from fastapi import FastAPI, UploadFile, File, HTTPException
from app.config import settings
from app.schemas import TextIngestRequest, IngestResponse, QuestionRequest, AnswerResponse, ExtractRequest
from app.services.chunking import chunk_text
from app.services.extract import extract_by_filename
from app.services.retrieval import Record, retriever
from app.services.qa import answer_question, extractive_summary
from app.services.knowledge_graph import simple_entity_graph
from app.services.model_adapters import layoutlmv3_status, qwen_vl_status

app = FastAPI(title=settings.app_name, version="0.1.0", description="Educational document intelligence MVP")

@app.get("/health")
def health(): return {"status": "ok", "environment": settings.app_env}

def _index(document_id: str, filename: str, text: str, metadata: dict):
    chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
    if not chunks: raise HTTPException(422, "No text could be extracted from the document")
    retriever.add([Record(document_id, filename, c.text, c.index, metadata) for c in chunks])
    return len(chunks)

@app.post("/documents/text", response_model=IngestResponse)
def ingest_text(payload: TextIngestRequest):
    count = _index(payload.document_id, payload.filename, payload.text, payload.metadata)
    return IngestResponse(document_id=payload.document_id, chunks_created=count, characters=len(payload.text))

@app.post("/documents/upload", response_model=IngestResponse)
async def upload_document(file: UploadFile = File(...), document_id: str | None = None):
    data = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(data) > settings.max_upload_mb * 1024 * 1024: raise HTTPException(413, "File exceeds configured upload limit")
    name = file.filename or "uploaded-file"
    try: text = extract_by_filename(name, data)
    except ValueError as exc: raise HTTPException(415, str(exc)) from exc
    except Exception as exc: raise HTTPException(422, f"Document extraction failed: {type(exc).__name__}") from exc
    doc_id = document_id or name
    count = _index(doc_id, name, text, {"content_type": file.content_type})
    return IngestResponse(document_id=doc_id, chunks_created=count, characters=len(text))

@app.post("/qa", response_model=AnswerResponse)
def qa(payload: QuestionRequest):
    result = answer_question(payload.question, retriever, payload.top_k, payload.document_id)
    return AnswerResponse(**result)

@app.get("/documents/{document_id}/summary")
def summarize(document_id: str):
    records = sorted([r for r in retriever.records if r.document_id == document_id], key=lambda r:r.chunk_index)
    if not records: raise HTTPException(404, "Document not found")
    text = " ".join(r.text for r in records)
    return {"document_id": document_id, "summary": extractive_summary(text), "method": "frequency-based extractive baseline"}

@app.post("/extract")
def extract_fields(payload: ExtractRequest):
    records = sorted([r for r in retriever.records if r.document_id == payload.document_id], key=lambda r:r.chunk_index)
    if not records: raise HTTPException(404, "Document not found")
    text = " ".join(r.text for r in records)
    import re
    out = {}
    for field in payload.fields:
        match = re.search(rf"(?im)^\s*{re.escape(field)}\s*[:=-]\s*(.+)$", text)
        out[field] = match.group(1).strip()[:500] if match else None
    return {"document_id": payload.document_id, "fields": out, "note": "Label-pattern baseline; not a trained information-extraction model."}

@app.get("/documents/{document_id}/knowledge-graph")
def graph(document_id: str):
    records = sorted([r for r in retriever.records if r.document_id == document_id], key=lambda r:r.chunk_index)
    if not records: raise HTTPException(404, "Document not found")
    return simple_entity_graph(" ".join(r.text for r in records))

@app.get("/models/status")
def model_status(): return {"layoutlmv3": layoutlmv3_status(), "qwen2_5_vl": qwen_vl_status()}
