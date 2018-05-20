# -*- coding:utf-8 -*-
import time

import etcd

from loggers.logger import log
from settings.setting import SETTING


class EtcdWrapper:
    def __init__(self, host, port):
        self.etcd_client = None
        self.etcd_host = host
        self.etcd_port = port

    def connect_etcd_cluster(self, connect_leader=False):
        while True:
            try:
                self.etcd_client = etcd.Client(
                    host=self.etcd_host, port=self.etcd_port, allow_reconnect=True, read_timeout=10)

                log.info(
                    'Connected to ETCD cluster: {}:{}'.format(self.etcd_host, self.etcd_port))

                if connect_leader:
                    leader = self.etcd_client.leader['clientURLs']
                    log.debug('leader: {}'.format(leader))
                    if leader is None:
                        return

                    leader = leader[0].split(':')[1][2:]
                    log.info('reconnect to leader: {}'.format(leader))
                    self.etcd_client = etcd.Client(
                        host=leader, port=self.etcd_port, allow_reconnect=True, read_timeout=10)

            except etcd.EtcdException:
                time.sleep(SETTING.ETCD_RECONNECT_WAIT_TIME)
                log.info('reconnect...')
                continue

            break

    def write(self, key, value):
        self.etcd_client.write(key, value)

    def create(self, key):
        try:
            self.etcd_client.read(key)
        except etcd.EtcdKeyNotFound:
            self.etcd_client.write(key, None, dir=True)

    def delete(self, key, isdir=False):
        try:
            self.etcd_client.delete(key, dir=isdir)
        except etcd.EtcdKeyNotFound:
            pass

    def get(self, key, default=None):
        if default is not None:
            v = default

        try:
            v = self.etcd_client.read(key).value
        except etcd.EtcdKeyNotFound:
            if default is not None:
                self.etcd_client.write(key, str(v))
            else:
                raise Exception('{} not exist'.format(key))
        except Exception as err:
            raise Exception('get error:{}'.format(str(err)))

        return v
