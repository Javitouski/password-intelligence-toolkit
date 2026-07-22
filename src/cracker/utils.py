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
        hashlib.sha256('test'.encode('utf-8')).hexdigest()
    return int(attempts / duration)

def entropy(charset: str, max_length:int) -> EntropyResult:
    """Calculates password entropy in bits and estimates rupture time based on benchmark."""
    if not charset or not max_length:
        return EntropyResult(entropy_bits=0.0, break_time_seconds=0.0, formatted_time='0 seconds')

    charset_size = len(charset)
    password_length = max_length
    
    # Entropy formula: H = L * log2(N)
    entropy_bits = password_length * math.log2(charset_size)
    combinations = 2 ** entropy_bits
    time_rupture = combinations / benchmark(1.0)
    read_time = ""

    if time_rupture < 60:
        read_time = f"{time_rupture:.2f} seconds"
    elif time_rupture < 3600:
        minutes = time_rupture / 60
        read_time = f"{minutes:.2f} minutes"
    elif time_rupture < 86400:
        hours = time_rupture / 3600
        read_time = f"{hours:.2f} hours"
    else:
        real_days = time_rupture / 86400
        read_time = f"{real_days:.2f} days"

    return EntropyResult(
        entropy_bits= entropy_bits,
        break_time_seconds= time_rupture,
        formatted_time= read_time,
    )