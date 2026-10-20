from pydantic import BaseModel, Field
from typing import Any

class TextIngestRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=120)
    filename: str = Field(min_length=1, max_length=255)
    text: str = Field(min_length=1, max_length=2_000_000)
    metadata: dict[str, Any] = Field(default_factory=dict)

class IngestResponse(BaseModel):
    document_id: str
    chunks_created: int
    characters: int

class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    document_id: str | None = None
    top_k: int = Field(default=4, ge=1, le=10)

class AnswerResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]
    disclaimer: str = "Baseline retrieval answer; verify against the original document."

class ExtractRequest(BaseModel):
    document_id: str
    fields: list[str] = Field(min_length=1, max_length=30)
