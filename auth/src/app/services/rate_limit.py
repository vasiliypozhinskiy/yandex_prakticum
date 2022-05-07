import datetime

from app.db.redis import redis_rate_limits
from app.utils.exceptions import RequestLimitReached


def check_rate_limit(user_id, rpm: int):
    pipe = redis_rate_limits.pipeline()
    now = datetime.datetime.now()
    key = f'{user_id}:{now.minute}'
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = pipe.execute()
    request_number = result[0]
    print(user_id, result, flush=True)
    if request_number > rpm:
        raise RequestLimitReached
