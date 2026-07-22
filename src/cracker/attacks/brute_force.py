import hashlib
import itertools
import time

from src.cracker.models import AttackResult


def attack(target_hash: str, charset: str, max_length: int) -> AttackResult | None:
    """Executes a sequential brute force attack up to max_length."""
    if not charset or not max_length:
        return None
    
    attempts = 0
    start = time.time()
    
    for i in range(1, max_length + 1):
        for combinations in itertools.product(charset, repeat=i):
            attempts += 1
            attempt_word = "".join(combinations)
            candidate_hash = hashlib.sha256(attempt_word.encode('utf-8')).hexdigest()
            
            if candidate_hash == target_hash:
                execution_time = time.time() - start
                
                # Prevent ZeroDivisionError for instant matches
                if execution_time == 0:
                    execution_time = 0.0001
                    
                velocity = attempts // execution_time
                
                return AttackResult(
                    word= attempt_word, 
                    attempts= attempts, 
                    velocity= int(velocity), 
                    execution_time= execution_time,
                )
    return None