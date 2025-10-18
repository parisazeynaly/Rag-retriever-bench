import os, glob
import lancedb
import pandas as pd
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from rich import print
import yaml
from .chunking import sliding_window

load_dotenv()

CFG = yaml.safe_load(open("configs/index.yaml"))
EMB = SentenceTransformer(CFG["embedding_model"])  # download on first run

DB_URI = os.getenv("LANCEDB_URI", "./db")
TABLE = os.getenv("TABLE", "docs")

def load_docs(root="data/docs"):
    paths = glob.glob(os.path.join(root, "**", "*"), recursive=True)
    for p in paths:
        if os.path.isdir(p):
            continue
        try:
            txt = open(p, "r", encoding="utf-8", errors="ignore").read()
            yield os.path.basename(p), txt
        except Exception as e:
            print(f"[yellow]skip {p}: {e}")

def build_index():
    rows = []
    for fname, text in load_docs():
        for chunk in sliding_window(text, CFG["chunk_size"], CFG["chunk_overlap"]):
            rows.append({"filename": fname, "text": chunk})
    df = pd.DataFrame(rows)
    if df.empty:
        print("[red]No documents found in data/docs. Add some .txt files and retry.")
        return

    print(f"Loaded {len(df)} chunks")

    vecs = EMB.encode(df["text"].tolist(), normalize_embeddings=CFG["normalize_embeddings"]).tolist()
    df["vector"] = vecs

    db = lancedb.connect(DB_URI)
    if TABLE in db.table_names():
        db.drop_table(TABLE)
    tbl = db.create_table(TABLE, data=df)
    print("[green]Index built:", tbl)

if __name__ == "__main__":
    build_index()
