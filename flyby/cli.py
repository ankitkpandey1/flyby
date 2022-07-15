import argparse
import importlib
import threading
from time import sleep

from flyby.brokers.redis import RQueue
from flyby.common.const import Settings
from flyby.worker import Worker

from flyby.common.logging import get_logger
from flyby.common.signals import SignalHandler


def main(args=None):
    """
    Main thread of Flyby which launches worker process
    """
    args = args or make_argument_parser().parse_args()
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
    broker = RQueue(url=REDIS_URL)

    running_queues = []
    active_threads = {}
    log.info("Booting up Flyby")
    sig = SignalHandler()
    while not sig.exit_now:
        all_queues = broker.get_all_active_queues()
        new_queues = list(set(all_queues) - set(running_queues))
        if len(new_queues) > 0:
            log.info(f"new queue is {new_queues}")
        for queue in running_queues:
            if queue not in all_queues and queue not in new_queues:
                log.info(f"dropping queue: {queue}")
                running_queues.remove(queue)

        for queue in new_queues:
            # launch a new worker
            worker = Worker(queue, broker, args.module, log)

            x = threading.Thread(target=worker.run, args=(), daemon=True)
            active_threads[queue] = x
            x.start()
            running_queues.append(queue)
        # sleep for a bit
        sleep(1)

        # cleanup dead threads
        # Broker cleans up queue when queue is empty.
        # But just when queue got empty, if new item gets enqueued
        # a new worker thread should get launch, these cleanup ensures that
        # it happens that way.
        dead_queues = []
        for queue, thread in active_threads.items():
            if not thread.is_alive():
                dead_queues.append(queue)

        for queue in dead_queues:
            del active_threads[queue]
            log.info(f"Running queue is {running_queues} and queue to drop is {queue}")
            
            # Ideally, queues get removed by themselves but in case concurrent system
            # we are forcing it so that new workers get launched
            if queue in running_queues:
                running_queues.remove(thread)

    log.info("Stopping Flyby")


def make_argument_parser():
    """
    Get cmd line arguments
    """
    parser = argparse.ArgumentParser(
        prog="flyby",
        description="Run Flyby workers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "module",
        help="the module to use. \
        This module should contain task.py file and \
        task_config dict defined",
    )

    parser.add_argument(
        "--config",
        help="configuration file containing env vars",
    )
    return parser
