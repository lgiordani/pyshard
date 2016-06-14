from pyshard import hash_functions as hf

def test_md5_hash_high_boundary():
    hashed_key = hf.hash_key("some random key", 'md5', 1e8)

    assert 0.70127616 + 1e-7 >= hashed_key >= 0.701276 - 1e-7

def test_md5_hash_low_boundary():
    hashed_key = hf.hash_key("some random key", 'md5', 1e2)

    assert 0.16 + 1e-7 >= hashed_key >= 0.16 - 1e-7

def test_sha256_hash():
    hashed_key = hf.hash_key("some random key", 'sha256', 1e8)

    assert 0.96105728 + 1e-7 >= hashed_key >= 0.96105728 - 1e-7
