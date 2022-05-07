from abc import abstractmethod, ABC
import uuid

import redis

from app.utils.utils import get_now_ms
from app.db.redis import redis_revoked_tokens, redis_log_out_all, redis_upd_roles
from app.core.config import REFRESH_TOKEN_EXP, ACCESS_TOKEN_EXP
from app.services.auth_services.jwt_service import JWT_SERVICE

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class BaseBlackList(ABC):
    @abstractmethod
    def add(self, **kwargs) -> None:
        pass

    @abstractmethod
    def is_ok(self, **kwargs) -> bool:
        pass


class TokenBlackList(BaseBlackList):
    def __init__(self, storage: redis.Redis, exp_time: int,  reason: str = ""):
        self.reason = reason
        self.storage = storage
        self.exp_time = exp_time

    def add(self, token: str) -> None:
        with tracer.start_as_current_span('TokenBlackList-add'):
            if token != "":
                self.storage.setex(
                    token,
                    self.exp_time,
                    self.reason
                )

    def is_ok(self, token: str) -> bool:
        with tracer.start_as_current_span('TokenBlackList-is_ok'):
            return not bool(self.storage.exists(token))


class UserIDBlackList(BaseBlackList):
    def __init__(self, storage: redis.Redis, exp_time: int):
        self.storage = storage
        self.exp_time = exp_time

    def add(self, user_id: uuid.UUID) -> None:
        
        with tracer.start_as_current_span('UserIDBlackList-add'):
            self.storage.setex(
                str(user_id),
                REFRESH_TOKEN_EXP,
                get_now_ms(),
            )

    def is_ok(self, access_token: str) -> bool:
        with tracer.start_as_current_span('UserIDBlackList-is_ok'):
            payload = JWT_SERVICE.get_access_payload(access_token)
            set_time = self.storage.get(str(payload.user_id))
            if set_time is None:
                return True  # no request to logout for this user
            set_time = int(set_time.decode())
            if payload.iat < set_time:
                return False  # logged in after request on logout
            return True


REVOKED_ACCESS = TokenBlackList(storage=redis_revoked_tokens, exp_time=ACCESS_TOKEN_EXP, reason='revoked')
LOG_OUT_ALL = UserIDBlackList(storage=redis_log_out_all, exp_time=REFRESH_TOKEN_EXP)
ROLES_UPDATE = UserIDBlackList(storage=redis_upd_roles, exp_time=REFRESH_TOKEN_EXP)