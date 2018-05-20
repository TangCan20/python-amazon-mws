#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import signal

from framework.batch_framework import BatchFrameworkMgr
from loggers.logger import log
from monitor.proc_monitor import refresh_configure_connection, ProcessMonitor
from service.globals import Globals
from web.services import run_web_service


def init():
    log.info('start to initialize')
    refresh_configure_connection(True)

    batch_framework_mgr = BatchFrameworkMgr()
    batch_framework_mgr.start()
    Globals.set_batch_framework_mgr(batch_framework_mgr)

    process_monitor = ProcessMonitor()
    process_monitor.start()
    Globals.set_process_monitor(process_monitor)
    log.info('init successfully')


def de_init():
    try:
        Globals.get_process_monitor().stop()
    except Exception as pass_error:
        log.error(str(pass_error))

    try:
        Globals.get_stat_wrapper().stop()
    except Exception as pass_error:
        log.error(str(pass_error))

    try:
        Globals.get_batch_framework_mgr().stop()
    except Exception as pass_error:
        log.error(str(pass_error))


def signal_handler(signum, frame):
    log.info('receive signal interrupt:{}'.format(signum))
    de_init()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    init()


if __name__ == '__main__':
    log.info('main start')

    try:
        main()
        run_web_service()
    except Exception as err:
        log.fatal('error:{}'.format(str(err)))
        de_init()

    log.info('main finish')
