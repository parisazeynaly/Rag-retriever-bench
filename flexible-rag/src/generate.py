from typing import List

def render_prompt(question: str, contexts: List[str]) -> str:
    ctx = "\n\n".join(f"[Doc {i+1}] {c}" for i, c in enumerate(contexts))
    return f"You are a helpful assistant. Use the following context to answer.\n{ctx}\n\nQuestion: {question}\nAnswer:"
