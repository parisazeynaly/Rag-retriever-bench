# Error Analysis (Concise, Student-Style)

We inspected 25 queries across 3 categories and noted typical failure modes.

## A) Entity Disambiguation
- Query: "Apple charging policy" → Retrieved docs about "battery charging" instead of "company refund policy".
- Cause: Keyword overlap ("charging") without company context.
- Fix: add organization-aware expansion; boost named entities.

## B) Compositional Constraints
- Query: "laptop under 900€ with 16GB RAM and OLED" → Retrieved either cheap or OLED, rarely both.
- Cause: Separate chunks satisfied different constraints.
- Fix: constraint-aware reranking (count satisfied attributes).

## C) Long-tail / Rare Terms
- Query: "Strehl ratio in amateur telescopes" → Dense helped; BM25 alone missed synonyms.
- Fix: keep hybrid and expand with synonyms in rewrite/HyDE.

## D) Conversational Coreference
- Query: "And what about its warranty?" → No previous antecedent in retrieved context.
- Fix: maintain short-term dialogue memory for pronoun resolution.

### Summary
Hybrid + rerank mitigates B and C. HyDE helps when the query is vague; smallest gains on highly specific keyword queries.
