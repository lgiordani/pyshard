import hashlib

def _normalize_number(num, boundary):
    # Normalizes between 0 and 1
    return float(num % boundary)/boundary

def hash_key(key, method, boundary):
    hash_function = getattr(hashlib, method)
    hashed_key_base10 = int(hash_function(key.encode()).hexdigest(), 16)

    return _normalize_number(hashed_key_base10, boundary)