import json
import numpy as np
from sentence_transformers import SentenceTransformer


def create_embeddings(corpus_path, output_path):
    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    texts = [c["text"] for c in corpus]

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(texts, show_progress_bar=True)

    np.save(output_path, embeddings)

    print("✅ Embeddings created!")