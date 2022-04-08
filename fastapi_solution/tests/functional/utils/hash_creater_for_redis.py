import hashlib


def create_hash_key(index: str, params: str) -> str:

    hash_key = hashlib.md5(params.encode()).hexdigest()
    return f"{index}:{hash_key}"
