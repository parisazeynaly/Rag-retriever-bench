from typing import List

def sliding_window(text: str, size: int = 400, overlap: int = 60) -> List[str]:
    tokens = text.split()
    out: List[str] = []
    i = 0
    step = max(1, size - overlap)
    while i < len(tokens):
        out.append(" ".join(tokens[i:i+size]))
        i += step
    return [c for c in out if c.strip()]
