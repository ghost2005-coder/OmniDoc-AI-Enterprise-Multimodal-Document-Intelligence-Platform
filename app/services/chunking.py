from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    index: int

def chunk_text(text: str, size: int = 900, overlap: int = 120) -> list[Chunk]:
    if size < 1 or overlap < 0 or overlap >= size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    clean = " ".join(text.split())
    if not clean:
        return []
    step = size - overlap
    return [Chunk(clean[i:i + size], idx) for idx, i in enumerate(range(0, len(clean), step))]
