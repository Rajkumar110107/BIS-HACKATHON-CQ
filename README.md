#  BIS AI Standard Recommendation System

AI-powered BIS Standard Recommendation System using **RAG (Retrieval-Augmented Generation)**.
Supports multi-domain queries with fast inference and **single-command execution**.

---

## Features

* 🔍 Multi-domain support (cement, aggregates, steel, soil, etc.)
* 🧠 Hybrid retrieval (semantic + keyword search)
* ⚡ Ultra-fast inference (~0.02s latency)
* 📚 Built on real BIS dataset (PDF → corpus)
* 🔄 No hardcoded mappings — fully data-driven

---

## Backend (Primary Evaluation)

The system is designed to run using a **single command**, as required for evaluation.

### ▶️ Run Inference

```bash
python inference.py --input sample.json --output result.json
```

---

## 📥 Input Format (`sample.json`)

```json
[
  {
    "id": 1,
    "query": "cement types and grades"
  }
]
```

---

## 📤 Output Format (`result.json`)

```json
[
  {
    "id": 1,
    "retrieved_standards": [
      "IS 269",
      "IS 8112",
      "IS 12269",
      "IS 1489",
      "IS 455"
    ],
    "latency_seconds": 0.02
  }
]
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Build Corpus (Only First Time)

```bash
python src/ingest.py
```

### 3. Run System

```bash
python inference.py --input sample.json --output result.json
```

---

##  System Architecture

* **Dataset**: BIS PDF (962 pages)
* **Chunking**: Text segmentation
* **Embeddings**: Sentence Transformers
* **Retrieval**:

  * BM25 (keyword)
  * Dense similarity (semantic)
* **Ranking**:

  * Query alignment
  * Consensus scoring
  * Frequency balancing

---

## Frontend (Optional)

A modern **React + Vite UI** has also been developed for demonstration.

### Features:

* Query input interface
* Real-time API interaction
* Card-based result display

> ⚠️ Note: Frontend is optional.
> Evaluation is based on backend single-command execution.

---

## 🏆 Hackathon Highlights

*  Fully automated pipeline
*  Single-command execution
*  Works across all domains
*  Fast, scalable, and robust

---

## 👨‍💻 Author

**Rajkumar R V**
**Subhiksha S**
**Rajanayagam K**
**Harish T**

---

## 📌 Note

This project focuses on backend intelligence and evaluation efficiency.
Frontend is included only for visualization and demo purposes.
