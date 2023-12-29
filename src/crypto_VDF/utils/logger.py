import inspect
import logging

from crypto_VDF import settings


def get_logger(location: str = __name__):
    log = logging.getLogger(location)
    log.setLevel(settings.log_level)
    return log


def set_level(logger: logging.Logger, level: int = logging.DEBUG):
    def deco(func):
        def wrapper(*args, **kwargs):
            _verbose = kwargs.get('_verbose', None)
            params = inspect.signature(func).parameters
            _verbose = next((True for param_name in params if param_name == '_verbose'), None)
            if _verbose is True:
                logger.setLevel(level)
            return func(*args, **kwargs)

        return wrapper

    return deco
