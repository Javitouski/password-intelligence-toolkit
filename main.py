import string
from src.cracker.engine import CrackerEngine

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
                cracker_result = CrackerEngine(target_hash, charset, max_length)
                entropy = cracker_result.entropy()
                if entropy.break_time_seconds > 300:
                    print(f"Stop! The password is too strong to break. Estimated crack time: {entropy.formatted_time}")
                else:
                    attack = cracker_result.attack()
                    if attack:
                        print(f"Match found!: {attack.word}")
                        print(f"Time: {attack.execution_time:.5f} seconds!")
                        print(f"Total of tries: {attack.attempts :,} try/tries")
                        print(f"The speed of math is: {attack.velocity : ,} words/seconds")
                    else:
                        print(f"We can't break the hash. Sorry!")
            elif options == 2:
                hash_input = input(f"Please, write the word to hash: ")
                hashing = CrackerEngine.create_hash(hash_input)
                print(f"The word to hash is: {hashing.plain_text} and it is: {hashing.hash_value}")
            elif options == 3:
                target_hash = input("Write the hash to broken:  ")
                dictionary_name = input(f"What is the name of the dictionary/file?: ")
                dcattack = CrackerEngine(target_hash)
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
        # except Exception as e:
            # print(f"Something went wrong. {e}")

if __name__ == "__main__":
    main()