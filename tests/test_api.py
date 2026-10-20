from fastapi.testclient import TestClient
from app.main import app
from app.services.retrieval import retriever

client = TestClient(app)

def setup_function():
    retriever.records = []
    if retriever.path.exists(): retriever.path.unlink()

def test_health(): assert client.get("/health").json()["status"] == "ok"

def test_ingest_and_qa():
    r = client.post("/documents/text", json={"document_id":"d1","filename":"note.txt","text":"Revenue: 120. The company expanded into Jaipur."})
    assert r.status_code == 200 and r.json()["chunks_created"] >= 1
    q = client.post("/qa", json={"question":"What is the revenue?","document_id":"d1"})
    assert q.status_code == 200 and "Revenue" in q.json()["answer"]

def test_missing_summary(): assert client.get("/documents/missing/summary").status_code == 404
