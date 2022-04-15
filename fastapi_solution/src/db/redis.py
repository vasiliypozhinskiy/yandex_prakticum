from abc import ABC, abstractmethod
from typing import Optional, Union


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    async def get(self, key: str):
        pass

    @abstractmethod
    async def set(self, key: str, value: Union[bytes, str], expire: int):
        pass

    @abstractmethod
    async def close(self):
        pass


redis: Optional[AbstractCache]


async def get_redis() -> AbstractCache:
    return redis
