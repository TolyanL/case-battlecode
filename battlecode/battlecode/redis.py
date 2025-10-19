import redis

from battlecode import settings as cfg

client = redis.Redis(
    host=cfg.REDIS_HOST,
    port=cfg.REDIS_PORT,
    db=0,
    decode_responses=True,
)
