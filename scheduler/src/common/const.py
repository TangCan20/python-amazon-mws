# -*- coding:utf-8 -*-


class _CONST(object):
    def __setattr__(self, *_):
        raise SyntaxError('Trying to change a constant value')

    TASK_TYPE = 'type'
    EMAIL_TASK = 'email'

    SUCCESS = 'success'
    FAILURE = 'fail'

    UTF_8 = 'utf8'

    ETCD_HOST = 'ETCD_SERVICE_SERVICE_HOST'
    ETCD_PORT = 'ETCD_SERVICE_SERVICE_PORT'

    METHOD_GET = 'GET'

    CUSTOMER_ID = 'cid'
    USER_NAME = 'name'
    IS_EXIST = 'exist'
    WISH_LIST = 'wish'
    EMAIL = 'email'
    UPDATE_DATE = 'update_date'

    MONITOR_MODULE = 'monitor'
    STAT_MODULE = 'stat'

    SYSTEM_NAME = 'ygmws'
    SUBSYSTEM_API = 'api'
    SUBSYSTEM_MGMT = 'mgmt'
    SUBSYSTEM_SCHEDULER = 'scheduler'
    SUBSYSTEM_EXECUTOR = 'executor'

    SYSTEM_FLASK_APP = '__' + SYSTEM_NAME.upper() + '_' + \
                       SUBSYSTEM_SCHEDULER.upper() + '_NODE__'

    THREAD_NUM = 'thread_num'
    PROCESSOR_CLS = 'processor_cls'
    BATCH_NAME = 'batch_name'
    TASK_QUEUE_NAME = 'task_queue_name'

    STAT_KEY = 'key'
    STAT_VALUE = 'value'
    SCHEDULER_STAT_TRIGGER_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_SCHEDULER + '_trigger_task_num'

    SCHEDULER_STAT_RECEIVE_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_SCHEDULER + '_receive_task_num'
    SCHEDULER_STAT_FORMAT_ERROR_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_SCHEDULER + '_format_error_task_num'
    SCHEDULER_STAT_PROCESS_ERROR_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_SCHEDULER + '_process_error_task_num'

    SCHEDULER_STAT_KEY_SET = [
        SCHEDULER_STAT_TRIGGER_TASK_NUM,
        SCHEDULER_STAT_RECEIVE_TASK_NUM,
        SCHEDULER_STAT_FORMAT_ERROR_TASK_NUM,
        SCHEDULER_STAT_PROCESS_ERROR_TASK_NUM
    ]


CONST = _CONST()
