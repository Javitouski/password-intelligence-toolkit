import hashlib
import time

from src.cracker.models import AttackResult


def dictionary_attack(target_hash:str,  dictionary: str) -> AttackResult | None:
    """Executes a dictionary-based attack reading line by line."""
    with open(dictionary, 'r', encoding='utf-8', errors='ignore') as file:
        start = time.time()
        attempts = 0
        
        for line in file:
            attempts += 1
            word = line.strip()
            candidate_hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
            
            if candidate_hash == target_hash:
                execution_time = time.time() - start
                return AttackResult(
                    word= word,
                    attempts= attempts,
                    execution_time=  execution_time
                )
        return None