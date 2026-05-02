import re


def extract_codes(text):
    # Match exact IS code formats correctly (e.g. "IS 269", "IS:269", "IS-269")
    pattern = r'\bIS\s*[:\-\.]?\s*(\d{2,5})\b'
    matches = re.findall(pattern, text)
    
    # Normalize to "IS XXXX"
    codes = [f"IS {match}" for match in matches]
    
    # Dedup and sort
    return sorted(list(set(codes)))