# -*- coding:utf-8 -*-
import time

from loggers.logger import log
from settings.setting import SETTING


class __Globals:
    __env_wrapper = None
    __etcd_wrapper = None
    __redis_wrapper = None
    __api_task_queue = None
    __stat_wrapper = None

    __process_monitor = None

    __heartbeat_dict = {}

    def __init__(self):
        pass

    def get_env_wrapper(self):
        return self.__env_wrapper

    def set_env_wrapper(self, env_wrapper):
        self.__env_wrapper = env_wrapper

    def get_etcd_wrapper(self):
        return self.__etcd_wrapper

    def set_etcd_wrapper(self, etcd_wrapper):
        self.__etcd_wrapper = etcd_wrapper

    def get_redis_wrapper(self):
        return self.__redis_wrapper

    def set_redis_wrapper(self, redis_wrapper):
        self.__redis_wrapper = redis_wrapper

    def get_stat_wrapper(self):
        return self.__stat_wrapper

    def set_stat_wrapper(self, stat_wrapper):
        self.__stat_wrapper = stat_wrapper

    def get_api_task_queue(self):
        return self.__api_task_queue

    def set_api_task_queue(self, task_queue):
        self.__api_task_queue = task_queue

    def get_process_monitor(self):
        return self.__process_monitor

    def set_process_monitor(self, process_monitor):
        self.__process_monitor = process_monitor

    def report_node_status(self, module_name):
        try:
            current_timestamp = time.time()
            log.debug('{} report status at {}'.format(module_name, current_timestamp))
            self.__heartbeat_dict[module_name] = current_timestamp
        except Exception as e:
            log.error('report node status err: {}'.format(e))

    def is_normal_status(self):
        try:
            current_timestamp = time.time()
            module_list = list(self.__heartbeat_dict.keys())
            for module in module_list:
                last = int(current_timestamp - self.__heartbeat_dict[module])
                if last > SETTING.NODE_REPORT_WAIT_TIME:
                    log.info('{} is not normal at {}'.format(module, current_timestamp))
                    return False
        except Exception as e:
            log.error('report node status err: {}'.format(e))

        log.debug('system is normal.')
        return True


Globals = __Globals()
