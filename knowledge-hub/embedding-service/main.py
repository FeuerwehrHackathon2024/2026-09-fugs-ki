from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Embedding Service")
model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_SIZE = 384


class EmbedRequest(BaseModel):
    texts: list[str]


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    dimension: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/dimension")
def dimension():
    return {"dimension": VECTOR_SIZE}


@app.post("/embed", response_model=EmbedResponse)
def embed(request: EmbedRequest):
    vectors = model.encode(request.texts, normalize_embeddings=True).tolist()
    return EmbedResponse(embeddings=vectors, dimension=VECTOR_SIZE)