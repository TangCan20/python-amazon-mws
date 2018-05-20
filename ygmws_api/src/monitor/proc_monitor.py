# -*- coding:utf-8 -*-
import sys
import threading
import time
import traceback

from common.const import CONST
from loggers.logger import log
from service.globals import Globals
from settings.setting import SETTING
from wrapper.env_wrapper import EnvWrapper
from wrapper.etcd_wrapper import EtcdWrapper
from wrapper.redis_queue import RedisQueue
from wrapper.redis_wrapper import RedisWrapper
from wrapper.stat_wrapper import StatWrapper


def refresh_configure_connection(is_init=False):
    if is_init:
        SETTING.reload_from_local()
        env_wrapper = EnvWrapper()
        env_wrapper.load_env()
        Globals.set_env_wrapper(env_wrapper)
        etcd_wrapper = EtcdWrapper(Globals.get_env_wrapper().etcd_host,
                                   Globals.get_env_wrapper().etcd_port)
        Globals.set_etcd_wrapper(etcd_wrapper)
        Globals.get_etcd_wrapper().connect_etcd_cluster()
        SETTING.reload_from_remote(Globals.get_etcd_wrapper())

        if len(SETTING.REDIS_PASSWORD) > 4:
            redis_wrapper = RedisWrapper(host=SETTING.REDIS_HOST,
                                         port=SETTING.REDIS_PORT,
                                         password=SETTING.REDIS_PASSWORD,
                                         max_connections=SETTING.MAX_REDIS_CONNECTION)
        else:
            redis_wrapper = RedisWrapper(host=SETTING.REDIS_HOST,
                                         port=SETTING.REDIS_PORT,
                                         max_connections=SETTING.MAX_REDIS_CONNECTION)

        log.info('init redis: {}:{}'.format(SETTING.REDIS_HOST, SETTING.REDIS_PORT))
        Globals.set_redis_wrapper(redis_wrapper)

        task_queue = RedisQueue(SETTING.API_TASK_QUEUE,
                                Globals.get_redis_wrapper().get_redis())
        Globals.set_api_task_queue(task_queue)

        stat_wrapper = StatWrapper(Globals.get_redis_wrapper().get_redis())
        Globals.set_stat_wrapper(stat_wrapper)
    else:
        Globals.get_etcd_wrapper().connect_etcd_cluster()
        SETTING.reload_from_remote(Globals.get_etcd_wrapper())


class ProcessMonitor:
    def __init__(self):
        self.is_running = False

    def monitor(self):
        counter = 0
        while self.is_running:
            try:
                if counter % SETTING.SETTING_REFRESH_INTERVAL == 0:
                    log.info('try to syn configure from remote...')
                    refresh_configure_connection()

                time.sleep(SETTING.MONITOR_SLEEP_TIME)
                Globals.report_node_status(CONST.MONITOR_MODULE)
                counter += 1
            except Exception as e:
                try:
                    log.error('monitor_thread error: {}'.format(str(e)))
                    log.error(sys.exc_info()[0])
                    log.error(traceback.format_exc())
                    time.sleep(SETTING.ERROR_WAIT_TIME)
                except Exception as pass_err:
                    log.debug(str(pass_err))

        log.info('monitor thread exit.')

    def start(self):
        log.info('try to start monitor thread')
        monitor_thred = threading.Thread(
            target=self.monitor, name='monitor_thread')
        self.is_running = True
        monitor_thred.start()

    def stop(self):
        log.info('try to stop monitor thread')
        self.is_running = False
