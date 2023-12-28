import logging

from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

from Settings.Config import LOG_FILE


def configure_logger():
    handler = RotatingFileHandler(
        filename=LOG_FILE,
        mode="a",
        maxBytes=10 * 1024 * 1024,
        backupCount=2,
        encoding=None,
        delay=True
    )

    formatter = ColoredFormatter(
        "[%(asctime)s] :: [%(log_color)s%(levelname)-4s%(reset)s] :: %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        log_colors={
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
        }
    )

    handler.setFormatter(formatter)

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.propagate = False

    return log


class Logger:
    def __init__(self):
        self.logger = configure_logger()

    def log_info(self, message):
        self.logger.info(message)

    def log_warn(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)


logger = Logger()
