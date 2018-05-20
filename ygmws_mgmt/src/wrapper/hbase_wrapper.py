# -*- coding:utf-8 -*-
import happybase

from loggers.logger import log


class HbaseWrapper:
    def __init__(self, hbase_endpoint, timeout):
        self.hbase_endpoint = hbase_endpoint
        self.timeout = timeout
        self.connection = None

    def connect(self):
        try:
            self.connection = happybase.Connection(self.hbase_endpoint,
                                                   timeout=self.timeout)
        except Exception as error:
            log.error(str(error))
            raise Exception(str(error))

    def disconnect(self):
        try:
            self.connection.close()
        except Exception as error:
            log.error(str(error))
            raise Exception(str(error))

    def create_table(self, tbl_name, data_dict):
        try:
            self.connection.create_table(
                tbl_name,
                data_dict
            )
            log.info('target table: {} create successfully.'.format(tbl_name))
        except Exception as e:
            log.error('target table: {} create fail.'.format(tbl_name, str(e)))
            raise Exception(str(e))

    def get_table(self, tbl_name):
        try:
            temp_table = self.connection.table(tbl_name)
            log.info('target table: {} get successfully.'.format(tbl_name))
        except Exception as e:
            log.error('target table: {} get fail.'.format(tbl_name, str(e)))
            raise Exception(str(e))
        return temp_table
