import os

import redis

_r = None


def get_redis():
    global _r
    if _r is None:
        _r = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB")),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
        )
    return _r


# para compatibilidad
r = get_redis()
