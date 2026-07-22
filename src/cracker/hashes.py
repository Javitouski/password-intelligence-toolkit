import hashlib
from src.cracker.models import HashResult

def create_hash(plain_text: str) -> HashResult:
    """Utility method to compute SHA-256 for a given string."""
    hashing = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    return HashResult(
        hash_value= hashing, 
        plain_text= plain_text,
    )