import os, yaml, pandas as pd, lancedb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from .router import decide_route

CFG = yaml.safe_load(open("configs/index.yaml"))
EMB = SentenceTransformer(CFG["text_embedding_model"])
DB_URI = os.getenv("LANCEDB_URI", "./db")

db = lancedb.connect(DB_URI)

def _bm25_over_table(tbl) -> BM25Okapi:
    df = tbl.to_pandas()
    col = "literal" if "literal" in df.columns else ("artistic" if "artistic" in df.columns else ("mood" if "mood" in df.columns else "image"))
    texts = df[col].fillna("").astype(str).tolist()
    if col == "image":  # no text
        texts = ["" for _ in texts]
    return BM25Okapi([t.split() for t in texts])

def route_search(query: str, route: str | None = None, topk: int = 10) -> pd.DataFrame:
    if route is None:
        route = decide_route(query).index
    tbl = db.open_table(route)
    vec = EMB.encode([query], normalize_embeddings=True)[0].tolist()
    dense = tbl.search(query_type="vector").vector(vec).limit(topk).to_pandas()
    # sparse (when textual)
    try:
        bm25 = _bm25_over_table(tbl)
        scores = bm25.get_scores(query.split())
        texts = tbl.to_pandas()
        col = "literal" if "literal" in texts.columns else ("artistic" if "artistic" in texts.columns else "mood")
        sp = pd.DataFrame({"image": texts["image"], "bm25": scores, "text": texts.get(col, "")})
        merged = pd.merge(dense, sp, on="image", how="left").fillna(0.0)
        if "_distance" in merged:
            merged["vec_sim"] = 1.0 - merged["_distance"]
        else:
            merged["vec_sim"] = 0.0
        alpha = float(CFG.get("bm25_boost", 0.4))
        merged["score"] = (1 - alpha) * merged["vec_sim"] + alpha * merged["bm25"]
        merged["route"] = route
        return merged.sort_values("score", ascending=False).head(topk).reset_index(drop=True)
    except Exception:
        dense["route"] = route
        return dense
