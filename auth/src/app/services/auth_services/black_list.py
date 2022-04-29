from abc import abstractmethod, ABC
import redis

from app.db.redis import  redis_revoked_tokens
from app.core.config import REFRESH_TOKEN_EXP, ACCESS_TOKEN_EXP


class BaseBlackList(ABC):
    @abstractmethod
    def add(self, **kwargs) -> None:
        pass

    @abstractmethod
    def is_ok(self, **kwargs) -> bool:
        pass


class RedisBlackList(BaseBlackList):
    def __init__(self, storage: redis.Redis, exp_time: int,  reason: str = ""):
        self.reason = reason
        self.storage = storage
        self.exp_time = exp_time

    def add(self, token: str) -> None:
        if token != "":
            self.storage.setex(
                token,
                self.exp_time,
                self.reason
            )

    def is_ok(self, token: str) -> bool:
        return not bool(self.storage.exists(token))


REVOKED_ACCESS = RedisBlackList(storage=redis_revoked_tokens, exp_time=ACCESS_TOKEN_EXP, reason='revoked')