# -*- coding: utf-8 -*-

import configparser
import traceback

from common.const import CONST
from loggers.logger import log


class _SETTING(object):
    API_TASK_QUEUE = CONST.SYSTEM_NAME + '_' + \
                     CONST.SUBSYSTEM_API + \
                     '_task_queue'

    SCHEDULER_TASK_QUEUE = CONST.SYSTEM_NAME + '_' + \
                           CONST.SUBSYSTEM_SCHEDULER + \
                           '_task_queue'

    GLOBAL_PREFIX = '/' + CONST.SYSTEM_NAME + '/global/settings/'
    IP_MAP_PREFIX = '/spider/run/ip_map/'
    IP_MAP_URL_PREFIX = '/spider/api/v1/ip_map'
    SETTING_PREFIX = '/' + CONST.SYSTEM_NAME + '/' + \
                     CONST.SUBSYSTEM_SCHEDULER + '/settings/'

    def __init__(self):
        self.etcd_wrapper = None
        self.configure_file = './configure.ini'
        self.config_list = [
            ('max_redis_connection', int, 'COMMON'),
            ('scheduler_thread_num', int, 'COMMON'),
            ('max_thread_queue_size', int, 'COMMON'),

            ('server_port', int, 'SERVER')
        ]

        self.global_config_list = [
            ('redis_host', str, 'REDIS'),
            ('redis_port', int, 'REDIS'),
            ('redis_password', str, 'REDIS'),
            ('setting_refresh_interval', float, 'COMMON'),
            ('monitor_sleep_time', float, 'COMMON'),
            ('request_connect_timeout', float, 'COMMON'),
            ('request_read_timeout', float, 'COMMON'),
            ('error_wait_time', float, 'COMMON'),
            ('etcd_reconnect_wait_time', float, 'COMMON'),
            ('max_task_fail_times', int, 'COMMON'),
            ('max_try_times', int, 'COMMON'),
            ('stat_queue_empty_wait_time', float, 'COMMON'),
            ('queue_empty_wait_time', float, 'COMMON'),
            ('queue_full_wait_time', float, 'COMMON'),
            ('node_report_wait_time', float, 'COMMON'),

            ('max_scheduler_queue_size', int, 'REDIS')
        ]

    def set_config(self, config_list, prefix_key=None):
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(self.configure_file)
        for item in config_list:
            try:
                name, value_type, section = item[0:3]
                func = item[3] if len(item) >= 4 else None

                if prefix_key:
                    key = '{}{}'.format(prefix_key, name.upper())
                    default_value = getattr(self, name.upper())
                    value = value_type(
                        self.etcd_wrapper.get(key, default_value))
                    config.set(section, name, value)
                    if func is not None:
                        value = func(value)
                else:
                    value = value_type(config.get(section, name))
                    if func is not None:
                        value = func(value)

                setattr(self, name.upper(), value)
            except Exception as error:
                log.error(str(error))
                log.error(traceback.format_exc())

        try:
            if prefix_key:
                with open(self.configure_file, 'w') as fp:
                    config.write(fp)
        except Exception as error:
            log.error(str(error))
            log.error(traceback.format_exc())

    def set_configure_file(self, configure_file):
        self.configure_file = configure_file

    def print_settings(self):
        for item in self.config_list:
            try:
                log.debug(
                    '{}: {}'.format(item[0], getattr(self, item[0].upper())))
            except Exception as error:
                log.error(str(error))
                log.error(traceback.format_exc())

        for item in self.global_config_list:
            try:
                log.debug(
                    '{}: {}'.format(item[0], getattr(self, item[0].upper())))
            except Exception as error:
                log.error(str(error))
                log.error(traceback.format_exc())

    def load_cfg_from_local(self):
        try:
            self.set_config(self.config_list)
            self.set_config(self.global_config_list)
        except Exception as error:
            log.error(str(error))
            log.error(traceback.format_exc())

    def load_cfg_from_remote(self):
        try:
            self.set_config(self.config_list, prefix_key=self.SETTING_PREFIX)
            self.set_config(self.global_config_list,
                            prefix_key=self.GLOBAL_PREFIX)
        except Exception as error:
            log.error(str(error))
            log.error(traceback.format_exc())

    def reload_from_local(self):
        self.load_cfg_from_local()
        self.print_settings()

    def reload_from_remote(self, etcd_wrapper=None):
        if etcd_wrapper:
            self.etcd_wrapper = etcd_wrapper

        self.load_cfg_from_remote()
        self.print_settings()


SETTING = _SETTING()
