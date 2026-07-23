import string
from src.cracker.engine import CrackerEngine

def test_entropy_time():
    charset = string.ascii_letters + string.digits + string.punctuation
    max_length = 9

    expected_entropy = 58.99

    engine = CrackerEngine(charset=charset, max_length=max_length)
    result = engine.entropy()

    assert round(result.entropy_bits, 2) == expected_entropy
