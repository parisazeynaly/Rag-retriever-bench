# RAG Workshop Suite (Monorepo)

This repo contains two complementary projects from the workshop:

1) **flexible-rag/** — lean, flexible RAG baseline: hybrid retrieval, optional re-ranking, HyDE stub, grading loop, and basic eval.
2) **semantic-router-art/** — multi-modal, multi-index retrieval with a **semantic router** that maps user intent to the right index (literal/artistical/mood/image).

## Quickstart
- See each subfolder's README for detailed steps.


## Reports & Evaluation (flexible-rag)
- `flexible-rag/reports/paper_template.md` and `.tex`: ready-to-fill report templates.
- `flexible-rag/scripts/eval_bench.py`: runs a small retrieval benchmark, writes `out/run.jsonl` and `out/metrics.json`.
- `flexible-rag/scripts/plot_latency_quality.py`: plots a latency–quality curve to `out/quality_latency.png`.
- Example eval data format under `flexible-rag/data/eval/`.

---

## Research Artifacts (flexible-rag)
- **Report (filled):** `flexible-rag/reports/paper_filled.md`
- **Figures:** `flexible-rag/reports/figures/quality_latency.png`
- **Results:** `flexible-rag/out/{benchmark.json,ablation.csv,error_analysis.md}`

### Reproduce (student-scale)
```bash
cd flexible-rag
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# (1) Prepare docs and build index
echo "Hello RAG world" > data/docs/sample.txt
python -m src. ingest

# (2) Run the lightweight eval & plot
python scripts/eval_bench.py --k 10
python scripts/plot_latency_quality.py
# artifacts: out/metrics.json, out/quality_latency.png
```
# Rag-retriever-bench
Lean RAG suite: hybrid retrieval, lightweight reranking, optional HyDE + a semantic router demo. Includes eval scripts, ablation and error analysis.”
