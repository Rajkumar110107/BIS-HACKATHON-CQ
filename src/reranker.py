from sentence_transformers import CrossEncoder


class ReRanker:
    def __init__(self):
        # lightweight model (fast ~1s total)
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query, docs, top_k=5):
        if not docs:
            return []

        pairs = [(query, d["text"]) for d in docs]
        scores = self.model.predict(pairs)

        for i, d in enumerate(docs):
            d["score"] = float(scores[i])

        docs = sorted(docs, key=lambda x: x["score"], reverse=True)

        return docs[:top_k]