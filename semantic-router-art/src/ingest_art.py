import os, glob, yaml
import lancedb, pandas as pd
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
from rich import print
from .features import color_histogram

load_dotenv()
CFG = yaml.safe_load(open("configs/index.yaml"))
EMB = SentenceTransformer(CFG["text_embedding_model"])

DB_URI = os.getenv("LANCEDB_URI", "./db")
IMG_DIR = "data/images"

def build_indices():
    # Prepare metadata
    rows = []
    for p in glob.glob(os.path.join(IMG_DIR, "*")):
        fname = os.path.basename(p)
        # infer simple captions from filename for demo (in a real system use captioner)
        if "sunset" in fname:
            literal = "Sunset over calm sea"
            artistic = "Impressionist warm evening light"
            mood = "warm, cozy, romantic"
        elif "forest" in fname:
            literal = "Misty forest pathway"
            artistic = "Naturalistic green tones"
            mood = "calm, fresh, exploring"
        elif "night" in fname:
            literal = "Night sky over village"
            artistic = "Moody deep blues"
            mood = "mysterious, blue, serene"
        else:
            literal = artistic = mood = fname
        rows.append({"image": fname, "literal": literal, "artistic": artistic, "mood": mood, "path": p})

    df = pd.DataFrame(rows)
    if df.empty:
        print("[red]No images in data/images")
        return

    db = lancedb.connect(DB_URI)

    # Literal index
    lit = df[["image", "literal"]].copy()
    lit["vector"] = EMB.encode(lit["literal"].tolist(), normalize_embeddings=CFG["normalize_embeddings"]).tolist()
    db.create_table("art_text_literal", data=lit, mode="overwrite")

    # Artistic index
    art = df[["image", "artistic"]].copy()
    art["vector"] = EMB.encode(art["artistic"].tolist(), normalize_embeddings=CFG["normalize_embeddings"]).tolist()
    db.create_table("art_text_artistic", data=art, mode="overwrite")

    # Mood index (treated as text)
    mood = df[["image", "mood"]].copy()
    mood["vector"] = EMB.encode(mood["mood"].tolist(), normalize_embeddings=CFG["normalize_embeddings"]).tolist()
    db.create_table("art_mood", data=mood, mode="overwrite")

    # Image color profile index
    img = df[["image", "path"]].copy()
    img["vector"] = img["path"].apply(color_histogram)
    db.create_table("art_image", data=img.drop(columns=["path"]), mode="overwrite")

    print("[green]Built indices: art_text_literal, art_text_artistic, art_mood, art_image")

if __name__ == "__main__":
    build_indices()
