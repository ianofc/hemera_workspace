import re
from fastapi import HTTPException

def sanitize_input(text: str) -> str:
    """Remove caracteres perigosos."""
    if not text:
        return ""
    clean = re.sub(r'<[^>]*>', '', text)
    return clean.strip()

def validate_age(age: int):
    if age < 0 or age > 120:
        raise HTTPException(status_code=400, detail="Idade inválida.")
    return age