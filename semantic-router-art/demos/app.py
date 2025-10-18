from fastapi import FastAPI
from pydantic import BaseModel
from .search import route_search

app = FastAPI(title="Semantic Router Art Demo")

class Q(BaseModel):
    query: str
    route: str | None = None  # optional override

@app.post("/route_search")
def api_route_search(q: Q):
    df = route_search(q.query, q.route, topk=10)
    # return only relevant columns
    cols = [c for c in df.columns if c in ("image", "literal", "artistic", "mood", "score", "route")]
    return {"results": df[cols].fillna("").to_dict(orient="records")}
