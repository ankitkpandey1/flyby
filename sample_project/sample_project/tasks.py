import logging
from time import sleep

log = logging.getLogger(__name__)


def start():
    log.info(f"starting START task")
    sleep(5)
    log.info(f"stopping START task")


def stop():
    log.info(f"starting STOP task")
    sleep(5)
    log.info(f"stopping STOP task")


def crash():
    log.info(f"starting CRASH task")
    sleep(5)
    log.info("Exception is coming")
    raise Exception("Critical exception happened")

    log.info(f"stopping CRASH task")  # noqa


task_config = {"start": start, "stop": stop, "crash": crash}
