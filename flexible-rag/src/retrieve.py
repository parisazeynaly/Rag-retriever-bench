import os, yaml
import lancedb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import pandas as pd

CFG = yaml.safe_load(open("configs/retrieval.yaml"))
EMB = SentenceTransformer("BAAI/bge-small-en-v1.5")

DB_URI = os.getenv("LANCEDB_URI", "./db")
TABLE = os.getenv("TABLE", "docs")

db = lancedb.connect(DB_URI)
tbl = db.open_table(TABLE)

# cache texts for BM25 (demo-only; for prod, store tokenized or use an FTS engine)
_texts = [r["text"] for r in tbl.to_pandas().to_dict("records")]
_bm25 = BM25Okapi([t.split() for t in _texts])

def hybrid_search(query: str, topk: int = 50) -> pd.DataFrame:
    vec = EMB.encode([query], normalize_embeddings=True)[0].tolist()
    dense = (
        tbl.search(query_type="vector")
           .vector(vec)
           .limit(topk)
           .to_pandas()
    )
    # sparse scores via BM25
    scores = _bm25.get_scores(query.split())
    sparse = pd.DataFrame({"text": _texts, "bm25": scores}).sort_values("bm25", ascending=False).head(topk)

    merged = pd.merge(dense, sparse, on="text", how="outer").fillna(0.0)
    # lancedb returns '_distance' where smaller is closer; convert to similarity-ish
    if "_distance" in merged:
        merged["vec_sim"] = 1.0 - merged["_distance"]
    else:
        merged["vec_sim"] = 0.0
    alpha = float(CFG.get("bm25_boost", 0.4))
    merged["score"] = (1 - alpha) * merged["vec_sim"] + alpha * merged["bm25"]
    return merged.sort_values("score", ascending=False).head(topk).reset_index(drop=True)
