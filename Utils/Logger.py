import logging

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

    formatter = logging.Formatter("[%(asctime)s] -> %(message)s", datefmt="%d-%b-%y %H:%M:%S")
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


class Logger:

    def __init__(self):
        self.logger = configure_logger()

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_info(self, message):
        self.logger.info(message)