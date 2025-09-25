import os
import sys

import redis

TESTING = "pytest" in sys.modules

_r = None


def get_redis():
    global _r
    if _r is None:
        if TESTING:
            from fakeredis import FakeStrictRedis

            _r = FakeStrictRedis(decode_responses=True)
        else:
            _r = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
                db=int(os.getenv("REDIS_DB")),
                # password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True,
            )
    return _r


r = get_redis()
