# -*- coding:utf-8 -*-

from common.const import CONST
from loggers.logger import log
from service.globals import Globals
from wrapper.redis_queue import RedisQueue


def clear_stat():
    stat_dict = {}
    redis_conn = Globals.get_redis_wrapper().get_redis()
    for series in CONST.STAT_KEY_SET:
        stat_list = []
        key_set = CONST.STAT_KEY_DICT.get(series)
        for key in key_set:
            item_num = redis_conn.set(key, 0)
            temp_dict = {CONST.STAT_KEY: key,
                         CONST.STAT_VALUE: str(item_num)}
            stat_list.append(temp_dict)
        stat_dict[series] = stat_list

    stat_list = []
    for key in CONST.REDIS_QUEUE_NAME_SET:
        try:
            redis_queue = RedisQueue(key, redis_conn)
            item_num = int(redis_queue.qsize())
        except Exception as error:
            log.info('{}, error:{}'.format(key, str(error)))
            item_num = -1

        temp_dict = {CONST.STAT_KEY: key,
                     CONST.STAT_VALUE: item_num}
        stat_list.append(temp_dict)

    stat_dict[CONST.QUEUE] = stat_list
    return stat_dict


def get_stat():
    stat_dict = {}
    redis_conn = Globals.get_redis_wrapper().get_redis()
    for series in CONST.STAT_KEY_SET:
        stat_list = []
        key_set = CONST.STAT_KEY_DICT.get(series)
        for key in key_set:
            try:
                item_num = int(redis_conn.get(key))
            except Exception as error:
                log.info('{}, error:{}'.format(key, str(error)))
                item_num = -1

            temp_dict = {CONST.STAT_KEY: key,
                         CONST.STAT_VALUE: int(item_num)}
            stat_list.append(temp_dict)
        stat_dict[series] = stat_list

    stat_list = []
    for key in CONST.REDIS_QUEUE_NAME_SET:
        try:
            redis_queue = RedisQueue(key, redis_conn)
            item_num = int(redis_queue.qsize())
        except Exception as error:
            log.info('{}, error:{}'.format(key, str(error)))
            item_num = -1

        temp_dict = {CONST.STAT_KEY: key,
                     CONST.STAT_VALUE: item_num}
        stat_list.append(temp_dict)

    stat_dict[CONST.QUEUE] = stat_list

    return stat_dict
