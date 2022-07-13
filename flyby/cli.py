import argparse
import importlib
import threading

from flyby.brokers.redis import RQueue
from flyby.common.const import Settings
from flyby.worker import Worker
from time import sleep
from flyby.common.logging import get_logger
from flyby.common.signals import SignalHandler


def main():
    args = make_argument_parser().parse_args()
    config_location = args.config
    task_module = args.module
    settings = Settings(_env_file=config_location, _env_file_encoding="utf-8")
    log = get_logger(__name__, "main", settings.LOG_LOCATION)
    try:
        importlib.import_module(task_module)
    except ImportError:
        log.error(f"Failed to import module {task_module}")

    REDIS_URL = (
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    )
    task_queue = RQueue(url=REDIS_URL)

    running_queues = []
    threads = []
    log.info("Booting up Flyby")
    sig = SignalHandler()
    while not sig.exit_now:
        all_queues = task_queue.get_all_active_queues()
        new_queues = list(set(all_queues) - set(running_queues))
        if len(new_queues) > 0:
            log.info(f"new queue is {new_queues}")
        for queue in running_queues:
            if queue not in all_queues and queue not in new_queues:
                log.info(f"dropping queue: {queue}")
                running_queues.remove(queue)

        for queue in new_queues:
            worker = Worker(queue, task_queue, args.module, log)

            x = threading.Thread(target=worker.run, args=(), daemon=True)
            threads.append(x)
            x.start()
            running_queues.append(queue)

        sleep(1)

    log.info("Stopping Flyby")


def make_argument_parser():
    parser = argparse.ArgumentParser(
        prog="flyby",
        description="Run Flyby workers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "module",
        help="the module to use",
    )

    parser.add_argument(
        "--config",
        help="configuration to use",
    )
    return parser
