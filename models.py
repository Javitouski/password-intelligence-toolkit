from dataclasses import dataclass
from typing import Optional

@dataclass
class EntropyResult:
    entropy_bits: float
    break_time_seconds: float
    formatted_time: str

@dataclass
class AttackResult:
    word: str
    attempts: int
    execution_time: float
    velocity: Optional[int] = None

@dataclass
class HashResult:
    plain_text: str
    hash_value: str