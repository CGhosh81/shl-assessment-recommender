# SHL GenAI Assessment Recommendation Engine

## Overview

This project implements a **GenAI-powered Assessment Recommendation System** using SHL’s product catalog.  
The system recommends the most relevant SHL assessments based on a recruiter’s natural-language hiring query.

The complete data preparation pipeline — including **web scraping, embedding generation, and FAISS indexing** — is implemented in **a single notebook** to keep the workflow simple and reproducible.

The recommendation engine is exposed as a **REST API** using FastAPI.  
No user interface (UI) is required.

---

## Problem Statement

Recruiters often describe hiring requirements in free-text form, for example:

> “I am hiring Java developers who can collaborate with business teams.”

The goal of this project is to automatically recommend the **most suitable SHL assessments** that match such hiring needs.

---

## Dataset

### Provided Dataset
- File: `Gen_AI_Dataset.xlsx`
- Columns:
  - `Query` – recruiter hiring intent
  - `Assessment_url` – relevant SHL assessment link

### SHL Product Catalog
Each assessment URL is scraped from the SHL website to extract structured metadata, including:
- Assessment name
- Description
- Duration
- Job levels
- Languages
- Test type
- Remote / adaptive support

The processed catalog is stored at:


data/product_catalog.json


---

## Approach

### 1. Data Collection
- Extract unique assessment URLs from the provided dataset
- Scrape SHL product catalog pages to collect structured assessment information

### 2. Embedding and Vector Indexing
- Generate semantic embeddings using the model:


sentence-transformers/all-MiniLM-L6-v2

- Index embeddings using **FAISS** for efficient similarity search
- Persist embeddings and the FAISS index to disk for reuse

All of these steps are implemented in:

notebooks/web_scraping_and_vector_database.ipynb

### 3. Recommendation Engine
- Encode recruiter queries into embeddings
- Perform nearest-neighbor search using FAISS
- Return the top-K most relevant assessments

### 4. Evaluation
- Ground truth is constructed from the provided dataset
- Evaluation metric used: **Recall@K**

Example results:

```
Recall@1 = 0.60
Recall@3 = 0.80
Recall@5 = 0.90
Recall@10 = 1.00
```

---

## API Design

The recommendation system is exposed as a REST API using **FastAPI**.

### Health Check

```
GET /health


Response:

{
  "status": "ok",
  "catalog_size": 65
}

Recommendation Endpoint
POST /recommend


Request body:

{
  "query": "I am hiring Java developers who can collaborate with business teams. The test should be around 40 minutes.",
  "top_k": 5
}


Response:

[
  {
    "name": "Core Java Entry Level",
    "url": "...",
    "duration_minutes": 40,
    "test_type": ["Knowledge & Skills"],
    "remote_support": true,
    "adaptive_support": false,
    "description": "..."
  }
]
```
### Project Structure
```
├── shl_recommender.py
│
├── notebooks/
│   └── web_scraping_and_vector_database.ipynb
│
├── data/
│   ├── Gen_AI_Dataset.xlsx
│   ├── product_catalog.json
│   └── embeddings/
│       ├── catalog_embeddings.npy
│       └── faiss.index
│
├── requirements.txt
└── README.md
```
How to Run
1. Install dependencies
```
pip install -r requirements.txt
```
2. Run the notebook

Execute all cells in:
```
notebooks/web_scraping_and_vector_database.ipynb
```

This will:

Scrape product data

Generate embeddings

Build and save the FAISS index

3. Start the API server
```
uvicorn shl_recommender:app --reload
```
4. Test the API

```
url = "http://127.0.0.1:8000/recommend"

payload = {
    "query": "I am hiring Java developers who can collaborate with business teams. The test should be around 40 minutes.",
    "top_k": 5
}

response = requests.post(url, json=payload)

results = response.json()
```


