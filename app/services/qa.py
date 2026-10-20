from .retrieval import LocalRetriever

def answer_question(question: str, retriever: LocalRetriever, top_k: int = 4, document_id: str | None = None) -> dict:
    hits = retriever.search(question, top_k=top_k, document_id=document_id)
    if not hits:
        return {"answer": "I could not find relevant evidence in the indexed documents. Try rephrasing the question or ingesting the relevant document.", "sources": []}
    # Extractive baseline: no LLM is called, so this avoids inventing a generative answer.
    excerpts = []
    sources = []
    for record, score in hits:
        excerpts.append(record.text)
        sources.append({"document_id": record.document_id, "filename": record.filename, "chunk_index": record.chunk_index, "score": round(score, 4), "excerpt": record.text[:500]})
    answer = "Relevant document passages:\n\n" + "\n\n---\n\n".join(excerpts)
    return {"answer": answer, "sources": sources}

def extractive_summary(text: str, max_sentences: int = 5) -> str:
    import re
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if len(sentences) <= max_sentences:
        return " ".join(sentences)
    # Simple frequency-based sentence ranking, preserving original order in final output.
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    freq = {}
    for word in words: freq[word] = freq.get(word, 0) + 1
    scored = []
    for i, sentence in enumerate(sentences):
        tokens = re.findall(r"[a-zA-Z]{3,}", sentence.lower())
        score = sum(freq.get(t, 0) for t in tokens) / max(len(tokens), 1)
        scored.append((score, i, sentence))
    chosen = sorted(scored, reverse=True)[:max_sentences]
    return " ".join(s for _, _, s in sorted(chosen, key=lambda x: x[1]))
