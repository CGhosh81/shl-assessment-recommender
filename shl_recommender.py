# shl_recommender.py

import json
import os
import numpy as np
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


DATA_DIR = "data"
EMBED_DIR = os.path.join(DATA_DIR, "embeddings")

CATALOG_PATH = os.path.join(DATA_DIR, "product_catalog.json")
EMBEDDINGS_PATH = os.path.join(EMBED_DIR, "catalog_embeddings.npy")
FAISS_INDEX_PATH = os.path.join(EMBED_DIR, "faiss.index")


with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")


doc_embeddings = np.load(EMBEDDINGS_PATH)


index = faiss.read_index(FAISS_INDEX_PATH)



app = FastAPI(
    title="SHL GenAI Assessment Recommender",
    version="1.0"
)


class RecommendRequest(BaseModel):
    query: str
    top_k: int = 5


class AssessmentResponse(BaseModel):
    name: str
    url: str
    duration_minutes: int | None
    test_type: list
    remote_support: bool
    adaptive_support: bool
    description: str | None



def recommend_assessments(query: str, top_k: int = 5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(catalog[idx])

    return results



@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "catalog_size": len(catalog)
    }


@app.post("/recommend", response_model=list[AssessmentResponse])
def recommend(request: RecommendRequest):
    results = recommend_assessments(
        request.query,
        request.top_k
    )

    return results
