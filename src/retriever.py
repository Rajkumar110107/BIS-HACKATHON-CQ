import json
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from src.utils import detect_domain


class Retriever:
    def __init__(self):
        with open("data/processed/corpus.json", "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

        self.texts = [d["text"] for d in self.corpus]

        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.embeddings = np.load("data/processed/embeddings.npy")
        self.embeddings = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )

        print("Building BM25...")
        tokenized = [t.lower().split() for t in self.texts]
        self.bm25 = BM25Okapi(tokenized)

        print("Retriever ready!")

    def search(self, query, top_k=5):
        # 🔥 STEP 1: DOMAIN DETECTION
        domain = detect_domain(query)
        query_lower = query.lower()

        # 🔥 STEP 2: QUERY EXPANSION (CRITICAL)
        if domain == "soil":
            query = query + " IS 2720 soil testing compaction"
        elif domain == "cement":
            query = query + " IS 269 IS 12269 cement types"
        elif domain == "steel":
            query = query + " IS 1786 reinforcement steel bars"

        # 🔥 STEP 3: EMBEDDING
        q_emb = self.model.encode([query], convert_to_tensor=True)
        q_emb = q_emb.cpu().numpy()
        q_emb = q_emb / (np.linalg.norm(q_emb) + 1e-10)

        dense_scores = np.dot(self.embeddings, q_emb[0])

        # 🔥 STEP 4: BM25
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        bm25_min = np.min(bm25_scores)
        bm25_max = np.max(bm25_scores)
        if bm25_max > bm25_min:
            bm25_scores = (bm25_scores - bm25_min) / (bm25_max - bm25_min)
        else:
            bm25_scores = np.zeros_like(bm25_scores)

        # 🔥 STEP 5: DOMAIN BOOSTING (STRONG)
        boost_scores = np.zeros_like(dense_scores)

        for i, text in enumerate(self.texts):
            t = text.lower()

            if domain == "soil" and ("soil" in t or "compaction" in t):
                boost_scores[i] += 1.0

            elif domain == "cement" and ("cement" in t or "concrete" in t):
                boost_scores[i] += 0.8

            elif domain == "steel" and ("steel" in t or "reinforcement" in t):
                boost_scores[i] += 0.8

            elif domain == "road" and ("road" in t or "bitumen" in t):
                boost_scores[i] += 0.5

            elif domain == "aggregate" and "aggregate" in t:
                boost_scores[i] += 0.5

        # 🔥 STEP 6: FINAL HYBRID SCORE
        final_scores = 0.45 * dense_scores + 0.35 * bm25_scores + boost_scores

        # 🔥 STEP 7: TAKE MORE RESULTS FOR PIPELINE
        top_indices = np.argsort(final_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "text": self.corpus[idx]["text"],
                "codes": self.corpus[idx]["codes"],
                "score": float(final_scores[idx])
            })

        return results
