import math
import time
import hashlib

from src.cracker.models import EntropyResult

def benchmark(duration: float = 1.0) -> int:
    """Measures hash calculation performance in hashes/second."""
    start = time.time()
    attempts = 0
    while (time.time() - start) < duration:
        attempts += 1
        hashlib.sha256('P4ssw0rd!'.encode('utf-8')).hexdigest()
    return int(attempts / duration)

def entropy(charset: str, password_length:int, hash_rate: float = 100_000_000.0) -> EntropyResult:
    """Calculates password entropy in bits and estimates rupture time based on benchmark."""
    if not charset or not password_length:
        return EntropyResult(entropy_bits=0.0, break_time_seconds=0.0, formatted_time='0 seconds')

    charset_size = len(charset)
    
    # Entropy formula: H = L * log2(N)
    entropy_bits = password_length * math.log2(charset_size)
    combinations = 2 ** entropy_bits
    break_time = combinations / hash_rate
    read_time = ""

    if break_time < 60:
        read_time = f"{break_time:.2f} seconds"
    elif break_time < 3600:
        minutes = break_time / 60
        read_time = f"{minutes:.2f} minutes"
    elif break_time < 86400:
        hours = break_time / 3600
        read_time = f"{hours:.2f} hours"
    else:
        real_days = break_time / 86400
        read_time = f"{real_days:.2f} days"

    return EntropyResult(
        entropy_bits= entropy_bits,
        break_time_seconds= break_time,
        formatted_time= read_time,
    )