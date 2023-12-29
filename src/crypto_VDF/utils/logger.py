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
            if _verbose is None:
                params = inspect.signature(func).parameters
                default_verbose = params.get('_verbose', {}).default
                _verbose = next((arg_value for i, arg_value in enumerate(args) if list(params)[i] == '_verbose'),
                                default_verbose)
            if _verbose is True:
                logger.setLevel(level)
            return func(*args, **kwargs)

        return wrapper

    return deco
