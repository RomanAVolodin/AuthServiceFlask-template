import redis

from settings.config import JWT_REDIS_HOST, JWT_REDIS_PORT

jwt_redis_blocklist = redis.StrictRedis(
    host=JWT_REDIS_HOST, port=JWT_REDIS_PORT, db=0, decode_responses=True
)
