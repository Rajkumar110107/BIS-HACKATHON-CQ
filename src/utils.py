import re


def extract_codes(text):
    pattern = r'\bIS\s*[:\-\.]?\s*(\d{2,5})\b'
    matches = re.findall(pattern, text)
    codes = [f"IS {match}" for match in matches]
    return sorted(list(set(codes)))


def detect_domain(query: str):
    q = query.lower()

    if "cement" in q or "concrete" in q:
        return "cement"
    elif "soil" in q or "compaction" in q:
        return "soil"
    elif "steel" in q or "reinforcement" in q:
        return "steel"
    elif "road" in q or "bitumen" in q:
        return "road"
    elif "aggregate" in q:
        return "aggregate"

    return "general"
