import datetime

from flask import request

from app.core.config import Config
from app.db.redis import redis_rate_limits
from app.utils.exceptions import RequestLimitReached
from app.services.auth_services.jwt_service import JWT_SERVICE
from app.utils.exceptions import InvalidToken


config = Config()


def check_rate_limit(user_id, rpm: int):
    pipe = redis_rate_limits.pipeline()
    now = datetime.datetime.now()
    key = f'{user_id}:{now.minute}'
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = pipe.execute()
    request_number = result[0]
    if request_number > rpm:
        raise RequestLimitReached


def limit_rate(func):
    def wrapper(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if not access_token:
            return func(*args, **kwargs)
        try:
            payload = JWT_SERVICE.get_access_payload(access_token)
            check_rate_limit(
                user_id=payload.user_id,
                rpm=config.RATE_LIMIT
            )
        except InvalidToken:
            pass
        return func(*args, **kwargs)
    return wrapper

