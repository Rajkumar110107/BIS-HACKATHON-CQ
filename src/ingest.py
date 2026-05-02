import os
import json
import re
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer

PDF_PATH = "data/raw/dataset.pdf"
CORPUS_PATH = "data/processed/corpus.json"
EMB_PATH = "data/processed/embeddings.npy"

model = SentenceTransformer("all-MiniLM-L6-v2")


# 🔹 Extract text from PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


# 🔹 Chunk text
def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks


# 🔹 Extract IS codes
def extract_codes(text):
    return list(set(re.findall(r'IS\s?\d{2,5}', text)))


def main():
    if not os.path.exists(PDF_PATH):
        print("❌ PDF not found:", PDF_PATH)
        return

    print("📄 Reading PDF...")
    text = extract_text_from_pdf(PDF_PATH)

    print("📏 Text length:", len(text))

    if len(text) < 100:
        print("❌ PDF text extraction failed (maybe scanned PDF)")
        return

    print("✂️ Chunking...")
    chunks = chunk_text(text)

    print("🔢 Total chunks:", len(chunks))

    corpus = []

    for i, chunk in enumerate(chunks):
        corpus.append({
            "text": chunk,
            "page": i + 1,
            "codes": extract_codes(chunk)
        })

    os.makedirs("data/processed", exist_ok=True)

    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)

    print("🧠 Creating embeddings...")
    embeddings = model.encode([c["text"] for c in corpus])

    np.save(EMB_PATH, embeddings)

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    main()