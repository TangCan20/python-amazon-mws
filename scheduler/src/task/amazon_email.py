# -*- coding:utf-8 -*-
import time

from common.const import CONST
from database.amazon_email_db import AmazonEmailDatabase
from loggers.logger import log
from service.globals import Globals
from settings.setting import SETTING
from wrapper.hbase_wrapper import HbaseWrapper


def amazon_email_process(task_data, base_dir):
    log.debug('amazon_email_process enter')
    task_dict = task_data.task_dict
    stat_wrapper = Globals.get_stat_wrapper()

    # try:
    #     hbase_wrapper = HbaseWrapper(SETTING.HBASE_ENDPOINT,
    #                                  SETTING.HBASE_CONNECT_TIMEOUT)
    #     hbase_wrapper.connect()
    #     amazon_db = AmazonEmailDatabase(hbase_wrapper)
    #     amazon_tbl = amazon_db.get_table()
    #     email = task_dict.get(CONST.EMAIL_TASK)
    #     email_target = amazon_tbl.row(email)
    #     if email_target != {}:
    #         is_exist = int(email_target[CONST.AMAZON_EMAIL_TABLE_EXIST].decode(CONST.UTF_8))
    #
    #         try:
    #             update_date = float(email_target[CONST.AMAZON_EMAIL_TABLE_UPDATE_DATE].decode(CONST.UTF_8))
    #             cur_time = float(time.time())
    #             ttl = cur_time - update_date
    #         except Exception as pass_error:
    #             log.debug(str(pass_error))
    #             ttl = SETTING.HBASE_AMZ_EMAIL_TTL
    #
    #         if is_exist or ttl < SETTING.HBASE_AMZ_EMAIL_TTL:
    #             stat_wrapper.increment(CONST.SCHEDULER_STAT_EXIST_TASK_NUM)
    #             log.info('target is exist {}.'.format(email))
    #             return
    # except Exception as err:
    #     stat_wrapper.increment(CONST.SCHEDULER_STAT_QUERY_HBASE_FAILURE_TASK_NUM)
    #     log.info(str(err))

    task_data.put_result(task_dict, CONST.SUCCESS)
    stat_wrapper.increment(CONST.SCHEDULER_STAT_SUCCESS_TASK_NUM)
