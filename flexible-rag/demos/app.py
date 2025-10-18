from fastapi import FastAPI
from pydantic import BaseModel
from src.loop import answer

app = FastAPI(title="Flexible RAG Demo")

class Q(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Q):
    return answer(q.question)
