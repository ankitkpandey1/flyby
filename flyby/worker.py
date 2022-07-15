import json
from inspect import signature

from flyby.common.utils import import_from


class Worker:
    def __init__(self, queue: str, broker: object, module: str, logger: object):
        """
        Initialize a new worker object

        Args:
            queue (str): queue
            broker : _description_
            module (str): _description_
            logger (object): _description_
        """
        self.logger = logger
        self.queue = queue
        self.broker = broker
        self.module = module

    def run(self):
        """
        Runs the worker thread until queue gets empty.
        If new task gets enqueued just when loop exits out,
        new worker thread will get launched to handle such situation.
        """

        while self.broker.get_queue_length(self.queue):
            payload: str = self.broker.dequeue(self.queue)
            payload: dict = json.loads(payload)
            self.logger.info(
                f"running worker against queue {self.queue} and payload is {payload}"
            )
            # module should define module.task with task_config dict
            tasks = import_from(self.module, "tasks")
       
            for func_name, func_args  in payload.items():
                try:
                    func = tasks.task_config.get(func_name)
                    if func:
                        # if task_name: None is passed as payload,
                        # it implies we are calling function without any args
                        # use signature to check param length
                        sig = signature(func)
                        if len(sig.parameters) > 0:
                            func_args = json.dumps(func_args)
                            func(func_args)
                        else:
                            func()
                    else:
                        self.logger.error(
                            f"no handler found for given task name {func_name}"
                        )
                except Exception as exp:
                    self.logger.error(f"Error while executing {func_name}: {str(exp)}")

        self.logger.info(f"stopping worker {self.queue}")
