from typing import Optional
from src.cracker.models import EntropyResult, AttackResult, HashResult
from src.cracker.utils import entropy
from src.cracker.attacks.brute_force import attack
from src.cracker.attacks.dictionary import dictionary_attack
from src.cracker.hashes import create_hash


class CrackerEngine:
    def __init__(self, target_hash: Optional[str] = None, charset: Optional[str] = None, max_length: Optional[int] = None) -> None:
        self.target_hash = target_hash
        self.charset = charset
        self.max_length = max_length
    
    def entropy(self)-> EntropyResult:
        if not self.charset or not self.max_length:
            return EntropyResult(entropy_bits=0.0, break_time_seconds=0.0, formatted_time='0 seconds')
        return entropy(self.charset, self.max_length)
    
    def attack(self, target_hash: Optional[str] = None) -> Optional[AttackResult]:
        hash_to_attack = target_hash or self.target_hash

        if not hash_to_attack or not self.charset or not self.max_length:
            return None
        
        return attack(hash_to_attack, self.charset, self.max_length )
    
    def dictionary_attack(self, dictionary: str, target_hash: Optional[str] = None) -> Optional[AttackResult]:
        hash_to_attack = target_hash or self.target_hash

        if not hash_to_attack or not dictionary:
            return None
        return dictionary_attack(hash_to_attack, dictionary)
    
    @staticmethod
    def create_hash(plain_text: str) -> HashResult:
        return create_hash(plain_text)
