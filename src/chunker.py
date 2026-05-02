import re


def clean_text(text):
    # Remove excessive leader dots or long lines often found in PDFs
    text = re.sub(r'[\.\-\_]{4,}', ' ', text)
    # Remove weird non-ascii encoding issues
    text = text.encode("ascii", "ignore").decode()
    # Normalize whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text, chunk_size=250, overlap=50):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap

    return chunks