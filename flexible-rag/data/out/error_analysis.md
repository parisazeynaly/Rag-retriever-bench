# Error Analysis (public-mini)

## A) Ambiguous noun
- Query: "What is a GPU used for?" → Top docs: d3 (GNN), d6 (Quantum), d9 (GPU). Correct is **d9** but appears rank #3.
- Fix: add hardware keyword boost or use reranker aware of device terms.

## B) Vague policy term
- Query: "charging policy" (not in dev set) → BM25 retrieves **d1** (Moon tides) due to word overlap.
- Fix: rewrite to "company battery charging policy" or prefer hybrid with entity boost.
