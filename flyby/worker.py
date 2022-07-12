from flyby.common.logging import get_logger

from flyby.common.utils import import_from
import json


class Worker:
    def __init__(self, queue, task_queue, module):
        self.logger = get_logger(__name__, type(self))
        self.queue = queue
        self.task_queue = task_queue
        self.module = module

    def run(self):

        while self.task_queue.get_queue_length(self.queue):
            payload = self.task_queue.dequeue(self.queue)
            payload = json.loads(payload)
            print(f"running worker against queue {self.queue} and payload is {payload}")
            tasks = import_from(self.module, "tasks")
            for k, v in payload.items():
                func = tasks.action_to_func_map.get(k)
                if func:
                    v = json.dumps(v)
                    func(v)
                else:
                    print(f"no handler found for given action {k}")

            payload = self.task_queue.dequeue(self.queue)

        print(f"stopping worker {self.queue}")
