# ⚡ BIS AI Standard Recommendation System

AI-powered BIS Standard Recommendation System using **RAG (Retrieval-Augmented Generation)**.
Supports multi-domain queries with fast inference and **single-command execution**.

---

## 🚀 Features

* 🔍 Multi-domain support (cement, aggregates, steel, soil, etc.)
* 🧠 Hybrid retrieval (semantic + keyword search)
* ⚡ Ultra-fast inference (~0.02s latency)
* 📚 Built on real BIS dataset (PDF → corpus)
* 🔄 No hardcoded mappings — fully data-driven

---

## ⚡ Backend (Primary Evaluation)

The system is designed for **single-command execution** for easy evaluation.

---

### 🚀 Recommended Execution (One Command)

```bash
.\run.bat
```

> ⚠️ Run in Windows PowerShell or Command Prompt

---

### 🧠 What This Does

The script automatically:

* 📦 Installs dependencies
* 📚 Builds corpus (only if missing)
* ⚡ Runs inference
* 📄 Displays final output

---

### 📜 run.bat

```bat
@echo off

echo 🚀 Starting BIS RAG System...

echo 📦 Installing dependencies...
pip install -r requirements.txt

if not exist data\processed\corpus.json (
    echo 📚 Building corpus...
    python src\ingest.py
) else (
    echo ✅ Corpus already exists, skipping...
)

echo ⚡ Running inference...
python inference.py --input sample.json --output result.json

echo 📄 Result:
type result.json

echo ✅ Done!
pause
```

---

## 🔁 Alternative Manual Execution

If required, the system can also be run manually:

```bash
pip install -r requirements.txt
python src/ingest.py
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

## ⚙️ Requirements

* Python (>= 3.9)
* pip

---

## 🧩 System Architecture

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

## 🌐 Frontend (Optional)

A modern **React + Vite UI** has also been developed for demonstration.

### Features:

* Query input interface
* Real-time API interaction
* Card-based result display

> ⚠️ Note: Frontend is optional.
> Evaluation is based on backend execution.

---

## 🏆 Hackathon Highlights

* ✅ Fully automated pipeline
* ✅ Single-command execution
* ✅ Works across all domains
* ✅ Fast, scalable, and robust

---

## 👨‍💻 Author

**Rajkumar R V**
**Subhiksha S**
**Rajanayagam K**
**Harish T**

---

## 📌 Note

* The system is fully automated using `run.bat`
* No manual setup required
* Designed for evaluator-friendly execution
* Frontend is included only for demonstration purposes
