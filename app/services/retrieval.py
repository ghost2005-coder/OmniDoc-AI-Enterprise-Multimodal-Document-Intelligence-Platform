from dataclasses import dataclass
from pathlib import Path
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Record:
    document_id: str
    filename: str
    text: str
    chunk_index: int
    metadata: dict

class LocalRetriever:
    """Simple local TF-IDF baseline. Replace with Chroma + sentence-transformers for semantic retrieval."""
    def __init__(self, store_path: str = "data/documents.json"):
        self.path = Path(store_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.records: list[Record] = []
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                rows = json.loads(self.path.read_text(encoding="utf-8"))
                self.records = [Record(**r) for r in rows]
            except (ValueError, TypeError):
                self.records = []

    def _save(self):
        self.path.write_text(json.dumps([r.__dict__ for r in self.records], ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, records: list[Record]):
        ids = {r.document_id for r in records}
        self.records = [r for r in self.records if r.document_id not in ids] + records
        self._save()

    def search(self, query: str, top_k: int = 4, document_id: str | None = None) -> list[tuple[Record, float]]:
        rows = [r for r in self.records if document_id is None or r.document_id == document_id]
        if not rows:
            return []
        corpus = [r.text for r in rows] + [query]
        matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus)
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        ranked = sorted(zip(rows, scores), key=lambda x: float(x[1]), reverse=True)[:top_k]
        return [(r, float(s)) for r, s in ranked if s > 0]

retriever = LocalRetriever()
