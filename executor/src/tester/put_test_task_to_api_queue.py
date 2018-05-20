# -*- coding:utf-8 -*-
import json

from loggers.logger import log
from settings.setting import SETTING
from wrapper.env_wrapper import EnvWrapper
from wrapper.etcd_wrapper import EtcdWrapper
from wrapper.redis_queue import RedisQueue
from wrapper.redis_wrapper import RedisWrapper


def test_connect():
    env_wrapper = EnvWrapper()
    env_wrapper.load_env()

    etcd_wrapper = EtcdWrapper(env_wrapper.etcd_host, env_wrapper.etcd_port)
    etcd_wrapper.connect_etcd_cluster()

    SETTING.set_configure_file(r'.\..\configure.ini')

    SETTING.reload_from_local()

    if len(SETTING.REDIS_PASSWORD) > 4:
        redis_wrapper = RedisWrapper(host=SETTING.REDIS_HOST,
                                     port=SETTING.REDIS_PORT,
                                     password=SETTING.REDIS_PASSWORD,
                                     max_connections=SETTING.MAX_REDIS_CONNECTION)
    else:
        redis_wrapper = RedisWrapper(host=SETTING.REDIS_HOST,
                                     port=SETTING.REDIS_PORT,
                                     max_connections=SETTING.MAX_REDIS_CONNECTION)
    redis_queue = RedisQueue(SETTING.API_TASK_QUEUE, redis_wrapper.get_redis())
    # task_dict = {'task_id': 'test'}
    # test_str = json.dumps(task_dict)

    test_str= 'hello'
    redis_queue.put(test_str)
    # s = redis_queue.get()
    #
    # if s != test_str:
    #     log.info('test not pass')
    # else:
    #     log.info('test pass')


if __name__ == '__main__':
    log.info('redis test start')

    try:
        test_connect()
    except Exception as err:
        log.fatal('error:{}'.format(str(err)))

    log.info('redis test finish')
