#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import signal
import sys
import threading
import time
import traceback

from loggers.logger import log
from service.globals import Globals
from settings.setting import SETTING
from web.services import run_web_service
from wrapper.env_wrapper import EnvWrapper
from wrapper.etcd_wrapper import EtcdWrapper
from wrapper.redis_wrapper import RedisWrapper
from common.const import CONST


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
                Globals.report_node_status(CONST.MONITOR_MODULE)
                if counter % SETTING.SETTING_REFRESH_INTERVAL == 0:
                    refresh_configure_connection()

                time.sleep(SETTING.MONITOR_SLEEP_TIME)
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


def de_init():
    try:
        Globals.get_process_monitor().stop()
    except Exception as pass_error:
        log.error(str(pass_error))


def init():
    try:
        refresh_configure_connection(True)
    except Exception as err:
        log.fatal(str(err))
        raise err


def run():
    process_monitor = ProcessMonitor()
    process_monitor.start()

    Globals.set_process_monitor(process_monitor)


def signal_handler(signum, frame):
    log.info('receive signal interrupt:{}'.format(signum))
    de_init()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    init()
    run()
    run_web_service()


if __name__ == '__main__':
    log.info('enter main...')

    try:
        main()
    except Exception as error:
        log.fatal(str(error))
        de_init()
        exit(0)

    log.info('exit main...')
