import string
from src.cracker.engine import CrackerEngine
WIDTH = 42


def main():
    options = 0
    print()
    print("=" * WIDTH)
    print("Password Intelligence Toolkit".center(WIDTH))
    print("=" * WIDTH)
    print()
    print(f" Select an option: ")
    print()
    print(f"    1.- Brute Force Attack ")
    print(f"    2.- Generate SHA-256 Hash")
    print(f"    3.- Dictionary Attack")
    print(f"    4.- Exit")
    print()
    while options != 4:
        try:
            options = int(input(f"Option: "))
            if options < 1 or options > 4:
                raise ValueError(f"[!] Invalid option.")
            if options == 1:
                target_hash = input("Target SHA-256 hash:  ")
                while True:
                    charset = ""
                    lower = input(f"Include lowercase letters? (y/N): ").lower()
                    upper = input(f"Include uppercase letters? (y/N): ").lower()
                    digits = input(f"Include digits? (y/N): ").lower()
                    symbols = input(f"Include symbols? (y/N): ").lower()                    
                    if lower == "y":
                        charset += string.ascii_lowercase
                    if upper == "y":
                        charset += string.ascii_uppercase
                    if digits == "y":
                        charset += string.digits
                    if symbols == "y":
                        charset += string.punctuation
                    if charset:
                        break
                    else:
                        print(f"[!] Select at least one character set.")
                max_length = int(input(f"What is the length of the password?: "))
                cracker_result = CrackerEngine(target_hash, charset, max_length)
                entropy = cracker_result.entropy()
                if entropy.break_time_seconds > 300:
                    print(f"Stop! The password is too strong to break. Estimated crack time: {entropy.formatted_time}")
                else:
                    attack = cracker_result.attack()
                    if attack:
                        print()
                        print("=" * WIDTH)
                        print("Attack Summary".center(WIDTH))
                        print("=" * WIDTH)
                        print()
                        print("[+] Password recovered successfully")
                        print()
                        print(f"{'Recovered Password':<18}: {attack.word}")
                        print(f"{'Execution Time':<18}: {attack.execution_time:.5f} s")
                        print(f"{'Attempts':<18}: {attack.attempts:,}")
                        print(f"{'Processing Rate':<18}: {attack.velocity:,} H/s")
                        print("=" * WIDTH)
                    else:
                        print(f"[-] No matching password found.")
            elif options == 2:
                hash_input = input(f"Plain text: ")
                hashing = CrackerEngine.create_hash(hash_input)
                print(f"SHA-256:: {hashing.plain_text} and it is: {hashing.hash_value}")
            elif options == 3:
                target_hash = input("Target SHA-256 hash:  ")
                dictionary_name = input(f"Dictionary file: ")
                dcattack = CrackerEngine(target_hash)
                print(f"[*] Starting dictionary attack on {dictionary_name}...")
                try:
                    print("[*] Running...")
                    attack_result = dcattack.dictionary_attack(dictionary_name)
                except FileNotFoundError:
                    print(f"[-] Dictionary file not found.")
                    attack_result = None
                if attack_result:
                    print(f"[+] Password found!: {attack_result.word}.")
                    print(f"[+] Total attempts: {attack_result.attempts}.")
                    print(f"[+] Execution time: {attack_result.execution_time:.5f} seconds.")
                else:
                    print(f"Something went wrong. Sorry!")
            else:
                print(f"Exiting Password Intelligence Toolkit...")
        except ValueError as e:
            print(f"[!] Invalid option. Please choose a value between 1 and 4. {e}")
        # except Exception as e:
            # print(f"Something went wrong. {e}")

if __name__ == "__main__":
    main()