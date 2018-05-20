# -*- coding:utf-8 -*-

class _CONST(object):
    def __setattr__(self, *_):
        raise SyntaxError('Trying to change a constant value')

    RESULT = 'result'
    STATUS = 'status'

    SUCCESS = 'SUCCESS'

    METHOD_POST = 'POST'
    METHOD_GET = 'GET'

    LIST = 'list'
    UTF_8 = 'utf8'

    ETCD_HOST = 'ETCD_SERVICE_SERVICE_HOST'
    ETCD_PORT = 'ETCD_SERVICE_SERVICE_PORT'

    TRUE = 'true'
    FALSE = 'false'

    MONITOR_MODULE = 'monitor'
    STAT_MODULE = 'stat'

    STAT_KEY = 'key'
    STAT_VALUE = 'value'

    SYSTEM_NAME = 'ygmws'
    SUBSYSTEM_API = 'api'
    SUBSYSTEM_MGMT = 'mgmt'
    SUBSYSTEM_SCHEDULER = 'framework'
    SUBSYSTEM_EXECUTOR = 'executor'
    SYSTEM_FLASK_APP = '__' + SYSTEM_NAME.upper() + '_' + \
                       SUBSYSTEM_API.upper() + '_NODE__'

    URL_PREFIX = '/' + SYSTEM_NAME + '/' + SUBSYSTEM_API + '/v1/'

    API_STAT_RECEIVE_REQ_AUTH_NUM = SYSTEM_NAME + '_' + SUBSYSTEM_API + \
                                    '_stat_receive_req_auth_num'

    API_STAT_KEY_SET = [
        API_STAT_RECEIVE_REQ_AUTH_NUM

    ]


CONST = _CONST()
