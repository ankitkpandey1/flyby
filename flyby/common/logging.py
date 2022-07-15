import inspect
import logging
from flyby.common.const import LOGFORMAT


def get_logger(module: str, name: str = None, filename: str = None):
    """
    Returns a logger object

    Args:
        module : module name
        name (str, optional): name which appears in logs.
                              Defaults to None.
        filename (str, optional): file where write log to.
                              Defaults to None.

    Returns:
        object: logger object
    """
    logger_fqn = module
    default_log_level = logging.DEBUG
    logging.basicConfig(level=default_log_level, format=LOGFORMAT, filename=filename)
    if name is not None:
        if inspect.isclass(name):
            name = name.__name__
        logger_fqn += "." + name

    return logging.getLogger(logger_fqn)
