from .retrieve import hybrid_search
from .grade import is_sufficient
from .generate import render_prompt

def answer(question: str, k_initial: int = 50, k_context: int = 8):
    cands = hybrid_search(question, topk=k_initial)
    if not is_sufficient(cands):
        # naive query expansion (placeholder)
        question = question + " keywords: overview, definition, examples"
        cands = hybrid_search(question, topk=k_initial)
    ctx = cands.head(k_context)["text"].tolist()
    prompt = render_prompt(question, ctx)
    return {"prompt": prompt, "contexts": ctx}
