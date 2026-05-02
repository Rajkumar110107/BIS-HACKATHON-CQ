import os
import json
from src.parser import extract_text_from_pdf
from src.chunker import chunk_text, clean_text
from src.utils import extract_codes


def build_corpus(pdf_folder, output_path):
    corpus = []

    # Ensure processed folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for file in os.listdir(pdf_folder):
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_folder, file)
        print(f"Processing {file}...")

        # 🔹 Extract text
        text = extract_text_from_pdf(pdf_path)

        # 🔹 Clean text
        text = clean_text(text)

        # 🔹 Chunk text (increased size for more context handled in chunk_text)
        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):
            words = chunk.split()
            # ❌ Skip very small chunks
            if len(words) < 40:
                continue

            # 🔹 Extract IS codes
            codes = extract_codes(chunk)

            # ❌ Skip chunks without IS codes (IMPORTANT)
            if not codes:
                continue

            # ❌ Quality filter: skip chunks that heavily consist of codes (likely an index page/table of contents)
            # which breaks context retrieval
            if len(codes) > 12 or len(codes) > (len(words) / 8):
                continue

            corpus.append({
                "text": chunk,
                "codes": codes,
                "source": file,
                "chunk_id": idx
            })

    # 🔹 Save corpus
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)

    print("Corpus built successfully!")
    print(f"Total valid chunks: {len(corpus)}")


# 🔹 Run standalone
if __name__ == "__main__":
    build_corpus("data/raw", "data/processed/corpus.json")