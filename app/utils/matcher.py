from rapidfuzz import fuzz
def is_match(q, t):
    return fuzz.partial_ratio(q.lower(), (t or "").lower()) > 60
