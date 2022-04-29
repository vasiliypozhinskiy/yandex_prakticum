from abc import abstractmethod, ABC

import redis
from datetime import datetime

from app.db.redis import redis_revoked_tokens, redis_log_out_all
from app.core.config import REFRESH_TOKEN_EXP, ACCESS_TOKEN_EXP, DATE_TIME_FORMAT
from app.services.auth_services.jwt_service import AccessPayload, JWT_SERVICE


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


class LogOutAllBlackList(BaseBlackList):
    def __init__(self, storage: redis.Redis, exp_time: int):
        self.storage = storage
        self.exp_time = exp_time

    def add(self, access_token: str) -> None:
        payload = JWT_SERVICE.get_access_payload(access_token)
        self.storage.setex(
            str(payload.user_id),
            REFRESH_TOKEN_EXP,
            datetime.strftime(datetime.now(), DATE_TIME_FORMAT),
        )


    def is_ok(self, access_token: str) -> bool:
        payload = JWT_SERVICE.get_access_payload(access_token)
        str_time = self.storage.get(str(payload.user_id))
        if str_time is None:
            return True  # no request to logout for this user

        iat = datetime.fromtimestamp(payload.iat)
        set_time = datetime.strptime(str_time.decode(), DATE_TIME_FORMAT)
        if iat < set_time:
            return False  # logged in after request on logout
        return True


REVOKED_ACCESS = RedisBlackList(storage=redis_revoked_tokens, exp_time=ACCESS_TOKEN_EXP, reason='revoked')
LOG_OUT_ALL = LogOutAllBlackList(storage=redis_log_out_all, exp_time=REFRESH_TOKEN_EXP)