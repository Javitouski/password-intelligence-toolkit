import string
import itertools
import time
import hashlib
import math
from typing import Optional, Any

def benchmark(duration: float = 1.0) -> int:
    start = time.time()
    attempts = 0
    while (time.time() - start) < duration:
        attempts += 1
        hashlib.sha256('test'.encode('utf-8')).hexdigest()
    return int(attempts / duration)

class Cracker:
    #Def Init, making a get and setters for target_hash, charset and max_length
    def __init__(self, target_hash: Optional[str] = None, charset: Optional[str] = None, max_length: Optional[int] = None) -> None:
        self.target_hash = target_hash #The hash to broken
        self.charset = charset # Amount of charset (a-z, A-Z, 0-9 and symbols)
        self.max_length = max_length # The max length of the password, that way we can do a better entropy calculate.

    # Def Entropy, How much time to take break the word/hash. If it take too much time, the program break the process.
    def entropy(self) -> dict[str, Any]:
        N = len(self.charset) # Transform the amount of characters to numbers, so we can calculate the entropy
        L = self.max_length # Length of the word/password
        H = L*math.log2(N) # Make the math to get entropy in bits
        combinations = 2 ** H # Calculate the amount of combinations
        time_rupture = combinations/benchmark(1.0) # Calculate the time taken for breaking a word/password
        read_time = ""

        # Transform the time so is more easily to read for the user.
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
        return{ 'Entropy': H,
                'breakTime': time_rupture,
                'human_time': read_time}

    # Def Attack, Brute Force for hash.  
    def attack(self) -> dict [str, Any] | None:
        attempts = 0 # Attemppts everytime the program make a combination and compare with the real hash
        start = time.time() # Start time so we can make the math ot the time taken broke a word/password
        
        # Bucle for where we define the max length, that way the program had an idea when finish
        for i in range(1, self.max_length + 1):
            # Bucle for where the program apply the brute force and make combinations to attack and get the hash
            for combinations in itertools.product(self.charset, repeat = i):
                attempts+=1 # Start the count of the attempts
                attempt_word = "".join(combinations) # Combine the letters and make the word
                hash_final = hashlib.sha256(attempt_word.encode('utf-8')).hexdigest() # Get the word formed by attempt_word and hashed to sha256
                if hash_final == self.target_hash: # Compare the hash create in hash_final with self.target_hash
                    execution_time = time.time() - start # If the   hash_final and the target_hash are the same, we calculate the time
                    if execution_time == 0: # Sometimes the program are susceptible to break when a variable is divisible for 0
                        execution_time = 0.0001 # So we give a tiny amount of time and avoid the posibility of breaking the program
                    velocity = attempts // finiexecution_timesh # Making the maths to get attemps to get the hash per time (finish)
                    # Return a dictionary of essential variable
                    return {'word': attempt_word, 
                            'attempts':attempts, 
                            'velocity':velocity, 
                            'time':execution_time}
        return None

    # Def Create Hash, This only work to hashing a word/password, not much relevant but usefull if you want to hash something.
    @staticmethod
    def create_hash(plainText: str) -> dict[str, Any] | None:
            hashing = hashlib.sha256(plainText.encode('utf-8')).hexdigest() # Hash the input and giving the value in a dictionary.
            return {'hashing': hashing, 
                    'value': plainText}
    
    # Def Dictionary Attack, Here we make an intelligent guess only if the user had a file/doc with some posible passwords/words.
    def dictionary_attack(self, dictionary: str) -> dict[str, Any] | None:
            # We open the dictionary and giving the read "r" option to  a file, encode the word to utf-8 and ignore errors in the file.
            with open(dictionary, 'r', encoding='utf-8', errors='ignore') as file:
                    start = time.time() # Adding the start time
                    attempts = 0 # Adding the attempts
                    # Bucle for where we recorre the file line by line getting the word of the file, hashing and comparing with the target_hash.
                    for line in file:
                        attempts += 1
                        word = line.strip() # Strip function remove white spaces from the 
                        candidate_hash = hashlib.sha256(word.encode('utf-8')).hexdigest()
                        if candidate_hash == self.target_hash:
                            execution_time = time.time() - start
                            return {'word': word,
                                    'attempts': attempts,
                                    'time': execution_time}
                    return None                    
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
                target_hash= input("Write the hash you want break:  ")
                while True:
                    charset = ""
                    lower = input(f"Include lowercasse? (s/n): ").lower()
                    upper = input(f"Include uppercase? (s/n): ").lower()
                    digits = input(f"Include digits? (s/n): ").lower()
                    symbols = input(f"Include symbols? (s/n): ").lower()                    
                    if lower == "s":
                        charset+= string.ascii_lowercase
                    if upper == "s":
                        charset+= string.ascii_uppercase
                    if digits == "s":
                        charset+= string.digits
                    if symbols == "s":
                        charset+= string.punctuation
                    if charset:
                        break
                    else:
                        print(f"Error! You need to choose at least one option.")
                max_length = int(input(f"What is the length of the password?: "))
                crackerResult = Cracker(target_hash, charset, max_length)
                entropy = crackerResult.entropy()
                if entropy['breakTime'] > 300:
                    print(f"Stop! The password is too strong to break. Time Rupture: {entropy['human_time']}")
                else:
                    attack = crackerResult.attack()
                    if attack:
                        print(f"WORD CATCH!: {attack['word']}")
                        print(f"Time: {attack['time']:.5f} seconds!")
                        print(f"Total of tries: {attack['attempts'] :,} try/tries")
                        print(f"The speed of math is: {attack['velocity'] : ,} words/seconds")
                    else:
                        print(f"We can't break the hash. Sorry!")
            elif options == 2:
                hash_input = input(f"Please, write the word to hash: ")
                try:
                    hashing = Cracker.create_hash(hash_input)
                except Exception as e:
                    print(f"Something went wrong. {e}")
                print(f"The word to hash is: {hashing['value']} and it is: {hashing['hashing']}")
            elif options == 3:
                target_hash= input("Write the hash to broken:  ")
                dictionary_name = input(f"What is the name of the dictionary/file?: ")
                dcattack = Cracker(target_hash)
                print(f"Starting the dictionary attack with the file {dictionary_name}...")
                try:
                    attack_result = dcattack.dictionary_attack(dictionary_name)
                except FileNotFoundError:
                    print(f"Sorry, the file {dictionary_name} was not found.")
                    attack_result = None
                if attack_result:
                    print(f"PASSWORD FOUND!: {attack_result['word']}.")
                    print(f"Time taken: {attack_result['time']:.5f} seconds.")
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