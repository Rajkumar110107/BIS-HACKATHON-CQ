import json
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi


class Retriever:
    def __init__(self):
        # Load corpus
        with open("data/processed/corpus.json", "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

        self.texts = [d["text"] for d in self.corpus]

        # 🔹 Embedding model
        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # 🔹 Load embeddings
        self.embeddings = np.load("data/processed/embeddings.npy")

        # 🔹 Normalize embeddings
        self.embeddings = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )

        # 🔹 BM25 setup
        print("Building BM25...")
        tokenized = [t.lower().split() for t in self.texts]
        self.bm25 = BM25Okapi(tokenized)

        print("Retriever ready!")

    def search(self, query, top_k=5):
        # 🔹 Query embedding
        q_emb = self.model.encode([query], convert_to_tensor=True)
        
        # Move to CPU for numpy operations
        q_emb = q_emb.cpu().numpy()
        q_emb = q_emb / (np.linalg.norm(q_emb) + 1e-10)

        # 🔹 Dense similarity (result is (N,))
        dense_scores = np.dot(self.embeddings, q_emb[0])

        # 🔹 BM25 scores
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # 🔹 Robust BM25 Normalization
        bm25_min = np.min(bm25_scores)
        bm25_max = np.max(bm25_scores)
        if bm25_max > bm25_min:
            bm25_scores = (bm25_scores - bm25_min) / (bm25_max - bm25_min)
        else:
            bm25_scores = np.zeros_like(bm25_scores)

        # 🔥 Hybrid scoring (slightly higher weight to dense for better context)
        final_scores = 0.55 * dense_scores + 0.45 * bm25_scores

        # 🔹 Top indices
        top_indices = np.argsort(final_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "text": self.corpus[idx]["text"],
                "codes": self.corpus[idx]["codes"],
                "score": float(final_scores[idx])
            })

        return results