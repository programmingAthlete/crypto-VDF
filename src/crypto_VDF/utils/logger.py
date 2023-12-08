import logging

from crypto_VDF import settings


def get_logger(location: str = __name__):
    log = logging.getLogger(location)
    log.setLevel(settings.log_level)
    return log
