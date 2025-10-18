import json, math
from collections import defaultdict

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def hit_at_k(qrels, run, k=5):
    gold = defaultdict(set)
    for r in qrels: gold[r["qid"].strip()].add(r["doc_id"])
    pred = defaultdict(list)
    for r in run: pred[r["qid"].strip()].append(r["doc_id"])
    num, den = 0, 0
    for q in gold:
        den += 1
        got = set(pred.get(q, [])[:k]) & gold[q]
        num += 1 if got else 0
    return num / max(den, 1)

def ndcg_at_k(qrels, run, k=10):
    rels = defaultdict(dict)
    for r in qrels: rels[r["qid"]][r["doc_id"]] = r.get("rel", 1)
    pred = defaultdict(list)
    for r in run: pred[r["qid"]].append((r["doc_id"], r.get("score", 0)))
    for q in pred: pred[q] = [d for d, _ in sorted(pred[q], key=lambda x: x[1], reverse=True)][:k]
    def dcg(g):
        return sum((g[i] / math.log2(i + 2) for i in range(len(g))))
    total, n = 0.0, 0
    for q, gold in rels.items():
        gains = [gold.get(doc, 0) for doc in pred.get(q, [])]
        ideal = sorted(gold.values(), reverse=True)[:k]
        if ideal:
            total += dcg(gains) / dcg(ideal)
            n += 1
    return total / max(n, 1)
