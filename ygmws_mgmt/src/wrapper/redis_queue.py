# -*- coding:utf-8 -*-

from common.const import CONST
from loggers.logger import log


class RedisQueue(object):
    def __init__(self, name, redis_conn, namespace='queue'):
        self.redis_conn = redis_conn
        self.key = '%s:%s' % (namespace, name)

    def reset_connection(self, redis_conn):
        self.redis_conn = redis_conn

    def get_redis(self):
        return self.redis_conn

    def qsize(self):
        return self.redis_conn.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        self.redis_conn.rpush(self.key, item)

    def get(self, block=False, timeout=None):
        try:
            if block:
                item = self.redis_conn.blpop(self.key, timeout=timeout)
            else:
                item = self.redis_conn.lpop(self.key)

            if item:
                item_result = item.decode(CONST.UTF_8)
            else:
                item_result = None
        except Exception as error:
            log.error(str(error))
            item_result = None

        return item_result
