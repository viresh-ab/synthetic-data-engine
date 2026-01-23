import re

PII_KEYWORDS = [
    "name", "email", "phone", "mobile",
    "aadhaar", "pan", "id"
]

def detect_pii(column_name: str) -> bool:
    col = column_name.lower()
    return any(k in col for k in PII_KEYWORDS)
