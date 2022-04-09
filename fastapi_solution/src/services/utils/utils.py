import hashlib


def create_hash_key(index: str, params: dict) -> str:
    """Хешируем ключ по индексу и параметрам запроса """
    sorted_params = str(sorted(params.items(), key=lambda x: x[0])).lower()
    hash_key = hashlib.md5(sorted_params.encode()).hexdigest()
    return f"{index}:{hash_key}"

