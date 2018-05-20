# -*- coding:utf-8 -*-
import signal

from loggers.logger import log
from monitor.proc_monitor import refresh_configure_connection, ProcessMonitor
from web.services import run_web_service
from service.globals import Globals


def de_init():
    try:
        Globals.get_process_monitor().stop()
        Globals.get_stat_wrapper().stop()
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
    Globals.get_stat_wrapper().start()


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
