from src.cracker.engine import CrackerEngine

def test_hash_creation():
    hash_input = "password"
    hash_result = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

    output = CrackerEngine.create_hash(hash_input)

    assert output.plain_text == hash_input
    assert output.hash_value == hash_result
