# -*- coding:utf-8 -*-
from common.const import CONST
from loggers.logger import log
from task.amazon_email import amazon_email_process

_TASK_FUNC_MAP = {
    CONST.EMAIL_TASK: amazon_email_process
}


def task_run(task_data, base_dir):
    log.debug('task_run enter')
    task_dict = task_data.task_dict
    log.info('{}'.format(task_data.task_dict))
    task_type = task_dict.get(CONST.TASK_TYPE)
    task_func = _TASK_FUNC_MAP.get(task_type)
    if task_func:
        task_func(task_data, base_dir)
    else:
        log.info('{} not support.'.format(task_type))

