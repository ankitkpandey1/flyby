from inspect import signature

from flyby.common.utils import import_from
import json


class Worker:
    def __init__(self, queue, task_queue, module, logger):
        self.logger = logger
        self.queue = queue
        self.task_queue = task_queue
        self.module = module

    def run(self):

        while self.task_queue.get_queue_length(self.queue):
            payload = self.task_queue.dequeue(self.queue)
            payload = json.loads(payload)
            self.logger.info(
                f"running worker against queue {self.queue} and payload is {payload}"
            )
            tasks = import_from(self.module, "tasks")
            for k, v in payload.items():
                try:
                    func = tasks.task_config.get(k)
                    if func:
                        sig = signature(func)
                        if len(sig.parameters) > 0:
                            v = json.dumps(v)
                            func(v)
                        else:
                            func()
                    else:
                        self.logger.error(f"no handler found for given action {k}")
                except Exception as e:
                    self.logger.error(str(e))

        self.logger.info(f"stopping worker {self.queue}")
