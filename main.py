import argparse
import string
import re
from src.cracker.engine import CrackerEngine
from src.cracker.utils import benchmark

def print_attack_result(attack):
    if attack:
        print(f"{'[+] Password found!':<20}: {attack.word}")
        print(f"{'[+] Total attempts':<20}: {attack.attempts:,.0f}")
        print(f"{'[+] Execution time':<20}: {attack.execution_time:.2f} seconds")
        if attack.velocity:
            print(f"{'[+] Velocity':<20}: {attack.velocity:,.0f} attempts/second")
    else:
        print("[-] Password not found within the given parameters.")

def is_valid_hash(hash_str):
    return bool(re.fullmatch(r'[a-fA-F0-9]{64}', hash_str))

def handle_hash(args):
    hashing = CrackerEngine.create_hash(args.text)
    print(f"[+] Plain text: {hashing.plain_text}")
    print(f"[+] SHA-256   : {hashing.hash_value}")

def handle_dict(args):
    if not is_valid_hash(args.target):
        print("[!] Error: Invalid SHA-256 hash format. Must be 64 hexadecimal characters.")
        return

    engine = CrackerEngine(args.target)
    attack = engine.dictionary_attack(args.wordlist)
    print_attack_result(attack)

def handle_brute(args):
    if not is_valid_hash(args.target):
        print("[!] Error: Invalid SHA-256 hash format. Must be 64 hexadecimal characters.")
        return
    charset = ""
    if args.lower:
        charset += string.ascii_lowercase
    if args.upper:
        charset += string.ascii_uppercase
    if args.digits:
        charset += string.digits
    if args.symbols:
        charset += string.punctuation

    if not charset:
        print("[!] Error: You must select at least one character set (--lower, --upper, --digits, --symbols)")
    else:
        engine = CrackerEngine(args.target, charset, args.length)

        print("[*] Calibrating hardware performance...")
        current_speed = benchmark()
        print(f"[*] Benchmark velocity: {current_speed:,.0f} H/s")

        entropy_result = engine.entropy(current_speed)
        if entropy_result.break_time_seconds > 300:
            print(f"[!] Target too strong. Estimated time: {entropy_result.formatted_time}")
        else:
            print("[*] Starting brute force attack...")
            attack = engine.attack()
            print_attack_result(attack)

def main():
    parser = argparse.ArgumentParser(description="Password Intelligence Toolkit - Advanced Hash Cracker")

    subparsers = parser.add_subparsers(dest="command", help="Available attack modes")

    hash_parser = subparsers.add_parser("hash", help="Generate a SHA-256 hash from plain text")
    hash_parser.add_argument("text", help="Plain text password to hash")

    dict_parser = subparsers.add_parser("dict", help="Perform a dictionary attack")

    dict_parser.add_argument("target", help="Target SHA-256 hash")
    dict_parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")

    brute_parser = subparsers.add_parser("brute", help="Perform a brute-force attack")
    brute_parser.add_argument("target", help="Target SHA-256 hash")
    brute_parser.add_argument("-l", "--length", type=int, required=True, help="Maximum password length")

    brute_parser.add_argument("--lower", action="store_true", help="Include lowercase letters")
    brute_parser.add_argument("--upper", action="store_true", help="Include uppercase letters")
    brute_parser.add_argument("--digits", action="store_true", help="Include numbers")
    brute_parser.add_argument("--symbols", action="store_true", help="Include special symbols")
    
    args = parser.parse_args()

    commands = {
        "hash": handle_hash,
        "dict": handle_dict,
        "brute": handle_brute
    }

    if args.command in commands:
        handler = commands[args.command]
        handler(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()