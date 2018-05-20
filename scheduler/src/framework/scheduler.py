from loggers.logger import log


class Scheduler:
    def __init__(self):
        pass

    def process(self, task_dict):
        log.info('start to process task {}'.format(task_dict))
