import re
from collections import defaultdict

def simple_entity_graph(text: str) -> dict:
    """Heuristic entity co-occurrence graph; replace with a validated NER model for serious use."""
    entities = re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", text)
    counts = defaultdict(int)
    for e in entities: counts[e] += 1
    nodes = [{"id": name, "label": name, "mentions": count} for name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0]))]
    # Co-occurrence in the same sentence is a weak candidate relation, not a verified fact.
    sentences = re.split(r"[.!?]", text)
    edges = set()
    for sentence in sentences:
        found = list(dict.fromkeys(re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", sentence)))
        for i, a in enumerate(found):
            for b in found[i+1:]:
                if a != b: edges.add((a, b))
    return {"nodes": nodes, "edges": [{"source": a, "target": b, "type": "co_occurs_in_sentence", "unverified": True} for a,b in sorted(edges)]}
