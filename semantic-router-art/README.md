# Semantic Router (Art) — Multi‑Modal Retrieval Demo

Goal: demonstrate **LLM/heuristic semantic routing** across multiple indices:
- literal text captions
- artistic/style captions
- mood keywords
- image color profile (toy feature) 

### Workflow
1) Put a few images in `data/images/` (PNG/JPG). Demo includes three synthetic images.
2) Run ingestion to build multiple LanceDB indices:
   - `art_text_literal`, `art_text_artistic`, `art_mood`, `art_image`
3) Call the `/route_search` endpoint with a text query (and optional `route` to override).

### Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Build indices from sample data
python -m src.ingest_art

# Start API
uvicorn demos.app:app --reload
# POST http://127.0.0.1:8000/route_search  { "query": "romantic blue evening painting" }
```

> Notes: image embeddings here are a **color histogram** (toy) so you can run without GPU.
Replace with CLIP or any vision model for real image semantics.
