# -*- coding: utf-8 -*-

import gc
import json
from queue import Queue
from threading import Thread
from time import sleep

from common.const import CONST
from framework.scheduler import Scheduler
from loggers.logger import log
from service.globals import Globals
from settings.setting import SETTING
from wrapper.redis_queue import RedisQueue


class BatchExecutor:
    def __init__(self, batch_name, processor_cls, thread_queue):
        self.is_running = False
        self.batch_processor = processor_cls()
        self.batch_name = batch_name
        self.thread_queue = thread_queue

    def run(self):
        while self.is_running:
            try:
                if self.thread_queue.empty():
                    sleep(SETTING.QUEUE_EMPTY_WAIT_TIME)
                    continue

                try:
                    task = self.thread_queue.get(block=False)
                except Exception as err:
                    log.debug(str(err))
                    sleep(SETTING.MONITOR_SLEEP_TIME)
                    continue

                if task is None:
                    sleep(SETTING.MONITOR_SLEEP_TIME)
                    continue

                self.batch_processor.process(task)
            except Exception as e:
                try:
                    err_msg = '{} ERROR in batch executor =[{}]'.format(self.batch_name, str(e))
                    log.error(err_msg)
                except Exception as passerr:
                    log.debug(str(passerr))

    def start(self):
        log.info('{} thread start'.format(self.batch_name))
        self.is_running = True
        Thread(target=self.run).start()
        return

    def stop(self):
        self.is_running = False
        log.info('{} thread stop'.format(self.batch_name))
        return

    def is_alive(self):
        return self.is_running


class BatchMonitor:
    def __init__(self, batch_name, batch_mgr):
        self.is_running = False
        self.batch_name = batch_name
        self.batch_mgr = batch_mgr

    def _run(self):
        log.info('{} monitor thread run'.format(self.batch_name))
        loop_count = 0
        while self.is_running:
            loop_count += 1
            try:
                if 0 == (loop_count % SETTING.SETTING_REFRESH_INTERVAL):
                    num_of_alive, num_of_dead = self.batch_mgr.get_status()
                    log.info('{} sub thread status,alive: {}, unalive: {}'.format(self.batch_name,
                                                                                  num_of_alive, num_of_dead))
                    if num_of_dead > 0:
                        self.batch_mgr.repair()
                        num_of_alive, num_of_dead = self.batch_mgr.get_status()
                        log.info('{} after repairing thread status, alive: {}, unalive: {}'.format(self.batch_name,
                                                                                                   num_of_alive,
                                                                                                   num_of_dead))

                    log.info('{} sub processor monitor thread try to call gc'.format(self.batch_name))
                    gc.collect()

                sleep(SETTING.MONITOR_SLEEP_TIME)
            except Exception as e:
                log.error('{} thread monitor error {}'.format(self.batch_name, str(e)))
                sleep(SETTING.ERROR_WAIT_TIME)

    def start(self):
        log.info('{} monitor thread start'.format(self.batch_name))
        self.is_running = True
        Thread(target=self._run).start()

    def stop(self):
        log.info('{} sub processor monior is going to stop.'.format(self.batch_name))
        self.is_running = False


class BatchManager:
    def __init__(self, batch_name, thread_num, processor_cls, thread_queue):
        self.thread_list = []
        self.thread_num = thread_num
        self.batch_name = batch_name
        self.processor_cls = processor_cls
        self.thread_queue = thread_queue

        log.info('{} with {} thread is going to init'.format(self.batch_name, thread_num))

    def release(self):
        try:
            for spec_thread in self.thread_list:
                log.info('{} try to realse thread'.format(self.batch_name))
                spec_thread.stop()
                self.thread_list.remove(spec_thread)
        except Exception as e:
            log.error('{} release error=[{}]'.format(self.batch_name, str(e)))

    def start(self):
        log.info('{} batch manager try to start:thread num:{}'.format(self.batch_name, self.thread_num))
        try:
            for i in range(self.thread_num):
                log.info('{} try to create thread:{}'.format(self.batch_name, i))
                thread_executor = BatchExecutor(self.batch_name, self.processor_cls, self.thread_queue)
                self.thread_list.append(thread_executor)
                thread_executor.start()
        except Exception as e:
            log.error('{} start error=[{}]'.format(self.batch_name, str(e)))
            self.release()
            pass

    def repair(self):
        log.info('thread manager try to repair')
        dead_thread_list = []
        try:
            for spec_thread in self.thread_list:
                if not spec_thread.is_alive():
                    dead_thread_list.append(spec_thread)

            for c_thread in dead_thread_list:
                spec_thread = BatchExecutor(self.batch_name, self.processor_cls)
                self.thread_list.append(spec_thread)
                spec_thread.start()
                self.thread_list.remove(c_thread)
        except Exception as e:
            log.error('{} start error=[{}]'.format(self.batch_name, str(e)))

    def get_status(self):
        log.info('{} thread manager try to get status'.format(self.batch_name))
        num_of_alive = 0
        num_of_dead = 0

        for crawler_thread in self.thread_list:
            if crawler_thread.is_alive():
                num_of_alive += 1
            else:
                num_of_dead += 1
        return num_of_alive, num_of_dead

    def stop(self):
        log.info('{} crawler manager try to stop'.format(self.batch_name))
        self.release()


class BatchFramework(object):
    def __init__(self, batch_name, task_queue_name, processor_cls, thread_num):
        self.task_queue_name = task_queue_name
        self.thread_num = thread_num
        self.processor_cls = processor_cls
        self.batch_name = batch_name
        self.thread_queue = Queue(SETTING.MAX_THREAD_QUEUE_SIZE)
        self.batch_mgr = BatchManager(self.batch_name, self.thread_num, self.processor_cls, self.thread_queue)
        self.batch_monitor = BatchMonitor(batch_name, self.batch_mgr)
        self.task_queue = RedisQueue(task_queue_name,
                                     Globals.get_redis_wrapper().get_redis())

        self.is_running = False

    def run(self):
        log.info('{} is going to run'.format(self.batch_name))
        while self.is_running:
            try:
                if self.thread_queue.qsize() >= SETTING.MAX_THREAD_QUEUE_SIZE:
                    sleep(SETTING.QUEUE_FULL_WAIT_TIME)
                    continue

                try:
                    if self.task_queue.empty():
                        sleep(SETTING.QUEUE_EMPTY_WAIT_TIME)
                        continue

                    task = self.task_queue.get()
                except Exception as err:
                    log.debug(str(err))
                    sleep(SETTING.MONITOR_SLEEP_TIME)
                    continue

                if task is None:
                    continue

                try:
                    task_dict = json.loads(task)
                    log.info(task_dict)
                except Exception as e:
                    log.error(str(e))
                    Globals.get_stat_wrapper().increment(CONST.SCHEDULER_STAT_FORMAT_ERROR_TASK_NUM)
                    raise e

                self.thread_queue.put(task_dict)
            except Exception as e:
                try:
                    err_msg = '{} ERROR in run =[{}]'.format(self.batch_name, str(e))
                    log.error(err_msg)
                    sleep(SETTING.MONITOR_SLEEP_TIME)
                except Exception as passerr:
                    log.debug(str(passerr))

    def start(self):
        log.info('{} start enter...'.format(self.batch_name))

        try:
            self.batch_mgr.start()
        except Exception as e:
            error_msg = '{} batch manager init error:{}'.format(self.batch_name, str(e))
            log.error(error_msg)
            raise Exception(error_msg)

        try:
            self.batch_monitor.start()
        except Exception as e:
            error_msg = '{} batch thread init error:{}'.format(self.batch_name, str(e))
            log.error(error_msg)
            self.batch_mgr.stop()
            raise Exception(error_msg)

        self.is_running = True
        self.run()

        log.info('{} start exit...'.format(self.batch_name))
        return

    def stop(self):
        log.info('{} is going to stop...'.format(self.batch_name))
        self.is_running = False
        self.batch_monitor.stop()
        self.batch_mgr.stop()


class BatchFrameworkMgr:
    def __init__(self):
        self.batch_init_set = [{
            CONST.BATCH_NAME: 'scheduler',
            CONST.TASK_QUEUE_NAME: SETTING.API_TASK_QUEUE,
            CONST.THREAD_NUM: SETTING.SCHEDULER_THREAD_NUM,
            CONST.PROCESSOR_CLS: Scheduler
        }]

        self.batch_instance_set = []

        for batch in self.batch_init_set:
            batch_framework = BatchFramework(batch.get(CONST.BATCH_NAME),
                                             batch.get(CONST.TASK_QUEUE_NAME),
                                             batch.get(CONST.PROCESSOR_CLS),
                                             batch.get(CONST.THREAD_NUM))
            self.batch_instance_set.append(batch_framework)

        self.is_start = False

    def start(self):
        if self.is_start:
            log.info('BatchFrameworkMgr has been started....')
            return

        self.is_start = True
        try:
            for batch in self.batch_instance_set:
                batch.start()
        except Exception as e:
            log.error(str(e))
            self.stop()

    def stop(self):
        if not self.is_start:
            log.info('BatchFrameworkMgr has not been started....')
            return

        for batch in self.batch_instance_set:
            try:
                batch.stop()
            except Exception as e:
                log.error(str(e))

        self.is_start = False
