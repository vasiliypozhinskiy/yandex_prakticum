import redis
from abc import ABC, abstractmethod
from app.db.redis import redis_ref_tokens


class BaseRefreshTokenStorage(ABC):

    exp_time: int

    @abstractmethod
    def is_token_exist(self, token):
        pass
    
    @abstractmethod
    def add_token(self, token):
        pass
    
    @abstractmethod
    def revoke_token(self, token):
        pass

    @abstractmethod
    def get_data(self, **kwargs):
        pass


class RedisRefreshTokenStorage(BaseRefreshTokenStorage):

    def __init__(self, exp_time: int, storage: redis.Redis):
        self.exp_time = exp_time
        self.storage = storage

    def is_token_exist(self, token) -> bool:
        return bool(self.storage.exists(token))
    
    
    def get_data(self, token) -> dict:
        raise NotImplementedError
    
    def add_token(self, token):
        self.storage.setex(
            token,
            self.exp_time,
            "",
        )
    
    def revoke_token(self, token):
        self.storage.delete(token)


REF_TOK_STORAGE = RedisRefreshTokenStorage(exp_time=600, storage = redis_ref_tokens)