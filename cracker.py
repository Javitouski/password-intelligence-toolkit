import string
import itertools
import time
import hashlib
import math
from typing import Optional, Any
from models import EntropyResult, AttackResult, HashResult


def benchmark(duration: float = 1.0) -> int:
    """Measures hash calculation performance in hashes/second."""
    start = time.time()
    attempts = 0
    while (time.time() - start) < duration:
        attempts += 1
        hashlib.sha256('test'.encode('utf-8')).hexdigest()
    return int(attempts / duration)


class Cracker:
    def __init__(self, target_hash: Optional[str] = None, charset: Optional[str] = None, max_length: Optional[int] = None) -> None:
        self.target_hash = target_hash
        self.charset = charset
        self.max_length = max_length

    def entropy(self) -> EntropyResult:
        """Calculates password entropy in bits and estimates rupture time based on benchmark."""
        if not self.charset or not self.max_length:
            return EntropyResult(entropy_bits=0.0, break_time_seconds=0.0, formatted_time='0 seconds')

        charset_size = len(self.charset)
        password_length = self.max_length
        
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

    def attack(self) -> AttackResult | None:
        """Executes a sequential brute force attack up to max_length."""
        if not self.charset or not self.max_length:
            return None
        
        attempts = 0
        start = time.time()
        
        for i in range(1, self.max_length + 1):
            for combinations in itertools.product(self.charset, repeat=i):
                attempts += 1
                attempt_word = "".join(combinations)
                candidate_hash = hashlib.sha256(attempt_word.encode('utf-8')).hexdigest()
                
                if candidate_hash == self.target_hash:
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

    @staticmethod
    def create_hash(plain_text: str) -> HashResult:
        """Utility method to compute SHA-256 for a given string."""
        hashing = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
        return HashResult(
            hash_value= hashing, 
            plain_text= plain_text,
        )

    def dictionary_attack(self, dictionary: str) -> AttackResult | None:
        """Executes a dictionary-based attack reading line by line."""
        with open(dictionary, 'r', encoding='utf-8', errors='ignore') as file:
            start = time.time()
            attempts = 0
            
            for line in file:
                attempts += 1
                word = line.strip()
                candidate_hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
                
                if candidate_hash == self.target_hash:
                    execution_time = time.time() - start
                    return AttackResult(
                        word= word,
                        attempts= attempts,
                        execution_time=  execution_time
                    )
            return None


def main():
    options = 0
    print(f"--- Select one of the options ---")
    print(f"1.- Enter the hash to crack ")
    print(f"2.- Enter the word to hash")
    print(f"3.- Try dictionary attack")
    print(f"4.- Exit")
    while options != 4:
        try:
            options = int(input(f"Please, choose an option: "))
            if options < 1 or options > 4:
                raise ValueError(f"That option is not available")
            if options == 1:
                target_hash = input("Write the hash you want break:  ")
                while True:
                    charset = ""
                    lower = input(f"Include lowercasse? (s/n): ").lower()
                    upper = input(f"Include uppercase? (s/n): ").lower()
                    digits = input(f"Include digits? (s/n): ").lower()
                    symbols = input(f"Include symbols? (s/n): ").lower()                    
                    if lower == "s":
                        charset += string.ascii_lowercase
                    if upper == "s":
                        charset += string.ascii_uppercase
                    if digits == "s":
                        charset += string.digits
                    if symbols == "s":
                        charset += string.punctuation
                    if charset:
                        break
                    else:
                        print(f"Error! You need to choose at least one option.")
                max_length = int(input(f"What is the length of the password?: "))
                cracker_result = Cracker(target_hash, charset, max_length)
                entropy = cracker_result.entropy()
                if entropy.break_time_seconds > 300:
                    print(f"Stop! The password is too strong to break. Time Rupture: {entropy.formatted_time}")
                else:
                    attack = cracker_result.attack()
                    if attack:
                        print(f"WORD CATCH!: {attack.word}")
                        print(f"Time: {attack.execution_time:.5f} seconds!")
                        print(f"Total of tries: {attack.attempts :,} try/tries")
                        print(f"The speed of math is: {attack.velocity : ,} words/seconds")
                    else:
                        print(f"We can't break the hash. Sorry!")
            elif options == 2:
                hash_input = input(f"Please, write the word to hash: ")
                try:
                    hashing = Cracker.create_hash(hash_input)
                except Exception as e:
                    print(f"Something went wrong. {e}")
                print(f"The word to hash is: {hashing.plain_text} and it is: {hashing.hash_value}")
            elif options == 3:
                target_hash = input("Write the hash to broken:  ")
                dictionary_name = input(f"What is the name of the dictionary/file?: ")
                dcattack = Cracker(target_hash)
                print(f"Starting the dictionary attack with the file {dictionary_name}...")
                try:
                    attack_result = dcattack.dictionary_attack(dictionary_name)
                except FileNotFoundError:
                    print(f"Sorry, the file {dictionary_name} was not found.")
                    attack_result = None
                if attack_result:
                    print(f"PASSWORD FOUND!: {attack_result.word}.")
                    print(f"Time taken: {attack_result.execution_time:.5f} seconds.")
                else:
                    print(f"Something went wrong. Sorry!")
            else:
                print(f"See you soon!")
        except ValueError as e:
            print(f"Sorry, thats not an available option. {e}")
        except Exception as e:
            print(f"Something went wrong. {e}")


if __name__ == "__main__":
    main()