import string
from typing import Optional, Any
from src.cracker.models import EntropyResult, AttackResult, HashResult
from src.cracker.utils import benchmark, entropy
from src.cracker.attacks.brute_force import attack
from src.cracker.attacks.dictionary import dictionary_attack
from src.cracker.hashes import create_hash


class CrackerEngine:
    def __init__(self, target_hash: Optional[str] = None, charset: Optional[str] = None, max_length: Optional[int] = None) -> None:
        self.target_hash = target_hash
        self.charset = charset
        self.max_length = max_length
    
    def entropy(self)-> EntropyResult:
        return entropy(self.charset, self.max_length)
    
    def attack(self) -> Optional[AttackResult]:
        return attack(self.target_hash, self.charset, self.max_length )
    
    def dictionary_attack(self, dictionary: str) -> Optional[AttackResult]:
        return dictionary_attack(self.target_hash, dictionary)
    
    @staticmethod
    def create_hash(plain_text: str) -> HashResult:
        return create_hash(plain_text)
