import inspect
import logging

from crypto_VDF import settings


def get_logger(location: str = __name__):
    log = logging.getLogger(location)
    log.setLevel(settings.log_level)
    return log


def check_arg_presence(arg: str, args, params, defaults):
    value = next((arg_value for i, arg_value in enumerate(args) if list(params)[i] == arg),
                 defaults)
    return value


def set_level(logger: logging.Logger, level: int = logging.DEBUG, hiding_level: int = logging.ERROR):
    """
    Set the logger level of the decorating function

    Args:
        logger: logger to which to set the log
        level: logging level to set
        hiding_level: logging level to hide all logs except errors

    Returns:

    """
    def deco(func):
        def wrapper(*args, **kwargs):
            params = inspect.signature(func).parameters
            defaults = {'_verbose': params.get('_verbose'), '_hide': params.get('_hide')}
            _verbose = kwargs.get('_verbose', None)
            if _verbose is None:
                _verbose = check_arg_presence(arg='_verbose', args=args, params=params, defaults=defaults)
            if _verbose is True:
                logger.setLevel(level)
            _hide = kwargs.get('_hide', None)
            if _hide is None:
                _hide = check_arg_presence(arg='_hide', args=args, params=params, defaults=defaults)
            if _hide is True:
                logger.setLevel(hiding_level)
            return func(*args, **kwargs)

        return wrapper

    return deco
