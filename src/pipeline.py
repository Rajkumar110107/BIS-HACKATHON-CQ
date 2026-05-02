import re
import math
from collections import defaultdict
from .retriever import Retriever


class Pipeline:
    def __init__(self):
        self.retriever = Retriever()

        self.stop_words = {
            "for", "the", "and", "a", "an", "in", "with", "of", "to", "on", "at",
            "from", "by", "is", "which", "that", "used", "made", "this", "are",
            "standard", "specification", "requirements", "bis", "code", "method",
            "general", "part", "section", "type", "test", "measure", "methods",
            "testing", "materials"
        }

        # 🔹 Precompute global DF for hub penalty
        self.code_df = defaultdict(int)
        for doc in self.retriever.corpus:
            for code in set(doc.get("codes", [])):
                self.code_df[code] += 1

    def _extract_keywords(self, text):
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        return {w for w in words if w not in self.stop_words}

    def run(self, query):
        # 🔥 Retrieve more candidates for better recall
        docs = self.retriever.search(query, top_k=70)

        query_keywords = self._extract_keywords(query)

        score_map = defaultdict(float)
        freq_map = defaultdict(int)
        fallback_codes = []

        for rank, doc in enumerate(docs):
            doc_score = doc["score"]
            chunk_text = doc["text"].lower()

            # 🔹 Keyword overlap
            matches = 0
            if query_keywords:
                matches = sum(1 for kw in query_keywords if kw in chunk_text)

            overlap_factor = 1.0 + 0.3 * matches

            # 🔥 Strong penalty for irrelevant chunks
            if matches == 0 and query_keywords:
                overlap_factor = 0.2

            # 🔹 Noise control
            noise_penalty = 0.6 if len(doc["codes"]) > 6 else 1.0

            # 🔹 Final chunk contribution
            chunk_weight = (doc_score / (rank + 1)) * overlap_factor * noise_penalty

            for code in doc["codes"]:
                fallback_codes.append(code)

                if code == "UNKNOWN" or len(code) < 4 or not code.startswith("IS "):
                    continue

                score_map[code] += chunk_weight
                freq_map[code] += 1

        # 🔹 Apply local consensus + global hub suppression
        alpha = 0.5

        for code in score_map:
            local_freq = freq_map[code]
            global_freq = self.code_df.get(code, 1)

            local_boost = math.log(local_freq + 1)
            if local_freq < 2:
                local_boost *= 0.3   # 🔥 stronger filtering

            hubness = math.log(global_freq + 2)
            hub_penalty = 1.0 / (1.0 + alpha * hubness)

            score_map[code] *= (local_boost * hub_penalty)

        # 🔹 Rank codes
        ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

        ranked_codes = [c for c, _ in ranked] + fallback_codes

        # 🔹 Final Top-5 (unique)
        seen = set()
        final = []

        for code in ranked_codes:
            if code not in seen and code.startswith("IS "):
                final.append(code)
                seen.add(code)

            if len(final) == 5:
                break

        return final
import re
import math
from collections import defaultdict
from .retriever import Retriever


class Pipeline:
    def __init__(self):
        self.retriever = Retriever()

        self.stop_words = {
            "for", "the", "and", "a", "an", "in", "with", "of", "to", "on", "at",
            "from", "by", "is", "which", "that", "used", "made", "this", "are",
            "standard", "specification", "requirements", "bis", "code", "method",
            "general", "part", "section", "type", "test", "measure", "methods",
            "testing", "materials"
        }

        # 🔹 Precompute global DF for hub penalty
        self.code_df = defaultdict(int)
        for doc in self.retriever.corpus:
            for code in set(doc.get("codes", [])):
                self.code_df[code] += 1

    def _extract_keywords(self, text):
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        return {w for w in words if w not in self.stop_words}

    def run(self, query):
        # 🔥 Retrieve more candidates for better recall
        docs = self.retriever.search(query, top_k=70)

        query_keywords = self._extract_keywords(query)

        score_map = defaultdict(float)
        freq_map = defaultdict(int)
        fallback_codes = []

        for rank, doc in enumerate(docs):
            doc_score = doc["score"]
            chunk_text = doc["text"].lower()

            # 🔹 Keyword overlap
            matches = 0
            if query_keywords:
                matches = sum(1 for kw in query_keywords if kw in chunk_text)

            overlap_factor = 1.0 + 0.3 * matches

            # 🔥 Strong penalty for irrelevant chunks
            if matches == 0 and query_keywords:
                overlap_factor = 0.2

            # 🔹 Noise control
            noise_penalty = 0.6 if len(doc["codes"]) > 6 else 1.0

            # 🔹 Final chunk contribution
            chunk_weight = (doc_score / (rank + 1)) * overlap_factor * noise_penalty

            for code in doc["codes"]:
                fallback_codes.append(code)

                if code == "UNKNOWN" or len(code) < 4 or not code.startswith("IS "):
                    continue

                score_map[code] += chunk_weight
                freq_map[code] += 1

        # 🔹 Apply local consensus + global hub suppression
        alpha = 0.5

        for code in score_map:
            local_freq = freq_map[code]
            global_freq = self.code_df.get(code, 1)

            local_boost = math.log(local_freq + 1)
            if local_freq < 2:
                local_boost *= 0.3   # 🔥 stronger filtering

            hubness = math.log(global_freq + 2)
            hub_penalty = 1.0 / (1.0 + alpha * hubness)

            score_map[code] *= (local_boost * hub_penalty)

        # 🔹 Rank codes
        ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

        ranked_codes = [c for c, _ in ranked] + fallback_codes

        # 🔹 Final Top-5 (unique)
        seen = set()
        final = []

        for code in ranked_codes:
            if code not in seen and code.startswith("IS "):
                final.append(code)
                seen.add(code)

            if len(final) == 5:
                break

        return final
