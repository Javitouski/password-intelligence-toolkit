from src.cracker.engine import CrackerEngine
import string

def test_brute_force_attack():
    objective = "abc"
    charset = string.ascii_lowercase

    engine = CrackerEngine(charset=charset, max_length=len(objective))
    hash_target = engine.create_hash(objective).hash_value

    result_of_attack = engine.attack(hash_target)

    assert result_of_attack is not None
    assert result_of_attack.word == objective
