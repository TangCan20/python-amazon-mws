# -*- coding:utf-8 -*-


class _CONST(object):
    def __setattr__(self, *_):
        raise SyntaxError('Trying to change a constant value')

    OPERATION = 'op'
    MONITOR_MODULE = 'monitor'
    METHOD_GET = 'GET'

    METHOD_DELETE = 'DELETE'
    UTF_8 = 'utf8'

    ETCD_HOST = 'ETCD_SERVICE_SERVICE_HOST'
    ETCD_PORT = 'ETCD_SERVICE_SERVICE_PORT'

    SYSTEM_NAME = 'ygmws'
    SUBSYSTEM_API = 'api'
    SUBSYSTEM_MGMT = 'mgmt'
    SUBSYSTEM_SCHEDULER = 'scheduler'
    SUBSYSTEM_EXECUTOR = 'executor'
    SYSTEM_FLASK_APP = '__' + SYSTEM_NAME.upper() + '_' + \
                       SUBSYSTEM_MGMT.upper() + '_NODE__'

    STAT_KEY = 'key'
    STAT_VALUE = 'value'

    API_STAT_RECEIVE_REQ_AUTH_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_API + \
                                    '_stat_receive_req_auth_num'

    API_STAT_KEY_SET = [
        API_STAT_RECEIVE_REQ_AUTH_NUM
    ]

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

    EXECUTOR_STAT_TRIGGER_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_EXECUTOR + '_trigger_task_num'

    EXECUTOR_STAT_RECEIVE_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_EXECUTOR + '_receive_task_num'
    EXECUTOR_STAT_FORMAT_ERROR_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_EXECUTOR + '_format_error_task_num'
    EXECUTOR_STAT_PROCESS_ERROR_TASK_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_EXECUTOR + '_process_error_task_num'

    EXECUTOR_STAT_KEY_SET = [
        EXECUTOR_STAT_TRIGGER_TASK_NUM,
        EXECUTOR_STAT_RECEIVE_TASK_NUM,
        EXECUTOR_STAT_FORMAT_ERROR_TASK_NUM,
        EXECUTOR_STAT_PROCESS_ERROR_TASK_NUM
    ]

    REDIS_QUEUE_NAME_SET = [
        'ygmws_api_task_queue',
        'ygmws_scheduler_task_queue',
        'ygmws_scheduler_result_queue',
        'ygmws_executor_task_queue'
    ]

    QUEUE = 'queue'

    STAT_KEY_SET = [
        SUBSYSTEM_API,
        SUBSYSTEM_SCHEDULER,
        SUBSYSTEM_EXECUTOR
    ]

    STAT_KEY_DICT = {
        SUBSYSTEM_API: API_STAT_KEY_SET,
        SUBSYSTEM_SCHEDULER: SCHEDULER_STAT_KEY_SET,
        SUBSYSTEM_EXECUTOR: EXECUTOR_STAT_KEY_SET
    }


CONST = _CONST()
