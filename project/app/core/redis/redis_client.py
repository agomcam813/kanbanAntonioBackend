# app/core/redis/redis_client.py
import os
import sys

import redis

TESTING = "pytest" in sys.modules

_r = None


def get_redis():
    """
    Returns a Redis client object.

    In testing mode, a fake Redis client is used.
    Otherwise, a real Redis client is used, either connecting to a remote
    Redis instance (Upstash TCP/TLS) or a local Redis
    instance (Docker or machine local).

    Returns:
        Redis client object.
    """
    global _r
    if _r is None:
        if TESTING:
            from fakeredis import FakeStrictRedis

            _r = FakeStrictRedis(decode_responses=True)
        else:
            redis_url = os.getenv("REDIS_URL")
            redis_token = os.getenv("REDIS_TOKEN")

            if redis_url and redis_token:
                # Redis remote (Upstash TCP/TLS)
                _r = redis.from_url(
                    redis_url,
                    password=redis_token,
                    decode_responses=True,
                )
            else:
                # Redis local (Docker or machine local)
                _r = redis.Redis(
                    host=os.getenv("REDIS_HOST"),
                    port=int(os.getenv("REDIS_PORT")),
                    db=int(os.getenv("REDIS_DB")),
                    password=os.getenv("REDIS_PASSWORD"),
                    decode_responses=True,
                )
    return _r


# Client global
r = get_redis()
