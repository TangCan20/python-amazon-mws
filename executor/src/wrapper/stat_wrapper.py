import threading
from queue import Queue
from time import sleep

from common.const import CONST
from loggers.logger import log
from service.globals import Globals
from settings.setting import SETTING


class StatWrapper:
    def __init__(self, redis_conn):
        self.stat_queue = Queue()
        self.is_running = False
        self.redis_conn = redis_conn

    def reset_connection(self, redis_conn):
        self.redis_conn = redis_conn

    def increment_to_redis(self, stat_dict):
        try:
            stat_num = stat_dict.get(CONST.STAT_VALUE)
            stat_key = stat_dict.get(CONST.STAT_KEY)
            self.redis_conn.incr(stat_key, amount=stat_num)
        except Exception as pass_error:
            log.debug(str(pass_error))

    def increment(self, item_name, item_num=1):
        try:
            log.debug('{}:{}'.format(item_name, item_num))
            if item_name not in CONST.SCHEDULER_STAT_KEY_SET or item_num <= 0:
                log.debug('not valid stat key')
                return

            data_dict = {
                CONST.STAT_KEY: item_name,
                CONST.STAT_VALUE: item_num
            }

            log.debug('{}'.format(data_dict))
            self.stat_queue.put(data_dict)
        except Exception as pass_error:
            log.info('[increment]{}'.format(str(pass_error)))

    def run(self):
        while self.is_running:
            try:
                Globals.report_node_status(CONST.STAT_MODULE)

                if self.stat_queue.empty():
                    log.debug('stat queue is empty...')
                    sleep(SETTING.STAT_QUEUE_EMPTY_WAIT_TIME)
                    continue

                try:
                    stat_dict = self.stat_queue.get(block=False)
                except Exception as err:
                    log.debug(str(err))
                    sleep(SETTING.MONITOR_SLEEP_TIME)
                    continue

                log.debug('stat {} start.'.format(stat_dict))
                self.increment_to_redis(stat_dict)

                log.debug('stat process successfully.')
            except Exception as e:
                try:
                    err_msg = 'ERROR in thread executor =[{}]'.format(str(e))
                    log.error(err_msg)
                except Exception as passerr:
                    log.debug(str(passerr))

        log.info('stat thread exit')

    def start(self):
        log.info('try to start stat thread')
        stat_thread = threading.Thread(
            target=self.run, name='stat_thread')
        self.is_running = True
        stat_thread.start()

    def stop(self):
        self.is_running = False
