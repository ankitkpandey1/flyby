import inspect
import logging
from flyby.common.const import LOGFORMAT

def get_logger(module, name=None, filename=None):
    logger_fqn = module
    default_log_level = logging.DEBUG
    #file_stream = logging.FileHandler(filename)
    logging.basicConfig(level=default_log_level, format=LOGFORMAT, filename=filename)
    if name is not None:
        if inspect.isclass(name):
            name = name.__name__
        logger_fqn += "." + name

    return logging.getLogger(logger_fqn)

