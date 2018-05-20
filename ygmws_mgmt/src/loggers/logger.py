# -*- coding:utf-8 -*-

import logging
import os
from logging import handlers

from common.const import CONST


def remove_log_file(storage_path, file_prefix):
    file_list = os.listdir(storage_path)
    for file in file_list:
        if file.startswith(file_prefix):
            os.remove(storage_path + file)


def init_logger(log_level):
    logger_name = CONST.SYSTEM_NAME + '_' + CONST.SUBSYSTEM_MGMT
    logger = logging.getLogger(logger_name)
    log_file_name = logger_name + '.log'
    storage_path = '/production/' + logger_name + '/log'

    file_name = storage_path + log_file_name

    if not os.path.exists(storage_path):
        os.makedirs(storage_path, exist_ok=True)
    else:
        remove_log_file(storage_path, log_file_name)

    fmt = '[%(asctime)s]'
    fmt += '-[%(levelname)s]'
    fmt += '-[%(process)d]'
    fmt += '-[%(threadName)s]'
    fmt += '-[%(thread)d]'
    fmt += '-[%(filename)s:%(lineno)s]'
    fmt += ' # %(message)s'
    formatter = logging.Formatter(fmt)

    handler = handlers.RotatingFileHandler(
        file_name, maxBytes=(16 * 1024 * 1024), backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)

    logger.setLevel(log_level)
    return logger


log = init_logger(logging.INFO)
