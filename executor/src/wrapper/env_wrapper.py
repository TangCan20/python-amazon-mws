# -*- coding:utf-8 -*-
import os
import random

from loggers.logger import log
from common.const import CONST


class EnvWrapper:
    etcd_host = ''
    etcd_port = 2379

    def __init__(self):
        pass

    def load_env(self):
        try:
            v = os.environ.get(CONST.ETCD_HOST, None)
            if v is None:
                error_str = '{} not set.'.format(CONST.ETCD_HOST)
                log.critical(error_str)
                raise Exception(error_str)

            a = v.split(',')
            self.etcd_host = str(a[random.randint(0, len(a) - 1)])

            v = os.environ.get(CONST.ETCD_PORT, None)
            if v is None:
                error_str = '{} not set.'.format(CONST.ETCD_PORT)
                log.critical(error_str)
                raise Exception(error_str)
            self.etcd_port = int(v)
        except Exception as err:
            log.error(str(err))
            raise Exception(str(err))
