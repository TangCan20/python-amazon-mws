# -*- coding:utf-8 -*-
import redis


class RedisWrapper(object):
    def __init__(self, **redis_kwargs):
        self.redis_conn = redis.Redis(**redis_kwargs)

    def get_redis(self):
        return self.redis_conn
