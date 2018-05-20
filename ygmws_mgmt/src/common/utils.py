# -*- coding:utf-8 -*-
from json import loads as json_loads

from common.const import CONST
from loggers.logger import log


def get_json_data_by_resp(resp):
    try:
        data_dict = json_loads(resp.content.decode(CONST.UTF_8))
    except Exception as err:
        log.error(str(err))
        return None
    return data_dict
