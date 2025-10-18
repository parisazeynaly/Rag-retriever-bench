#!/usr/bin/env python
"""Run a tiny benchmark over sample queries and produce metrics + a run file.

Usage:
  python scripts/eval_bench.py --k 10

It expects:
  data/eval/queries.jsonl      # {"qid":"q1","text":"..."}
  data/eval/qrels.jsonl        # {"qid":"q1","doc_id":"<filename>#<chunk_idx>","rel":1}
It produces:
  out/run.jsonl                # ranked list
  out/metrics.json             # {"hit@5":..., "hit@10":..., "ndcg@10":...}
"""
import os, json, argparse, pandas as pd
from src.retrieve import hybrid_search
from src.eval import load_jsonl, hit_at_k, ndcg_at_k

def main(k):
    os.makedirs("out", exist_ok=True)
    run = []
    for q in load_jsonl("data/eval/queries.jsonl"):
        qid, text = q["qid"], q["text"]
        df = hybrid_search(text, topk=k)
        for rank, row in enumerate(df.itertuples(), start=1):
            doc_id = f"{getattr(row,'filename','doc')}"  # fallback
            if hasattr(row, 'text'):
                # create a synthetic id by hashing chunk text index if available
                doc_id = f"{doc_id}#{rank}"
            run.append({"qid": qid, "doc_id": doc_id, "score": float(getattr(row,"score", 0.0)), "rank": rank})
    with open("out/run.jsonl", "w", encoding="utf-8") as f:
        for r in run: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    qrels = list(load_jsonl("data/eval/qrels.jsonl"))
    hit5 = hit_at_k(qrels, run, k=5)
    hit10 = hit_at_k(qrels, run, k=10)
    ndcg10 = ndcg_at_k(qrels, run, k=10)
    metrics = {"hit@5": hit5, "hit@10": hit10, "ndcg@10": ndcg10}
    with open("out/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print(metrics)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()
    main(args.k)
