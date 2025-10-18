from typing import List
from dataclasses import dataclass

@dataclass
class ScoredDoc:
    text: str
    score: float

class NoOpReranker:
    def rerank(self, query: str, docs: List[ScoredDoc]) -> List[ScoredDoc]:
        return sorted(docs, key=lambda d: d.score, reverse=True)

try:
    from lancedb.rerankers import ColbertReranker as _ColBERT
except Exception:
    _ColBERT = None

class ColbertWrapper:
    def __init__(self, model_name: str):
        if _ColBERT is None:
            raise RuntimeError("ColBERT not available; ensure compatible lancedb extras are installed")
        self.model = _ColBERT(model_name)
    def rerank(self, query: str, docs: List[ScoredDoc]) -> List[ScoredDoc]:
        texts = [d.text for d in docs]
        scores = self.model.score(query, texts)
        pairs = sorted(zip(texts, scores), key=lambda x: x[1], reverse=True)
        return [ScoredDoc(t, float(s)) for t, s in pairs]
