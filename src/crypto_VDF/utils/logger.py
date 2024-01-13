import inspect
import logging

from crypto_VDF import settings


def get_logger(location: str = __name__):
    log = logging.getLogger(location)
    log.setLevel(settings.log_level)
    return log


def check_arg_presence(arg: str, func, args):
    params = inspect.signature(func).parameters
    default_verbose = params.get(arg, {}).default
    arg_value = next((arg_value for i, arg_value in enumerate(args) if list(params)[i] == '_verbose'),
                     default_verbose)
    return arg_value


def set_level(logger: logging.Logger, level: int = logging.DEBUG):
    def deco(func):
        def wrapper(*args, **kwargs):
            _verbose = kwargs.get('_verbose', None)
            if _verbose is None:
                _verbose = check_arg_presence(arg='_verbose', func=func, args=args)
            if _verbose is True:
                logger.setLevel(level)
            _hide = kwargs.get('_hide', None)
            if _hide is None:
                _hide = check_arg_presence(arg='_hide', func=func, args=args)
            if _hide is True:
                logger.setLevel(logging.CRITICAL)
            return func(*args, **kwargs)

        return wrapper

    return deco
