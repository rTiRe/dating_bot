import logging

from config.settings import settings


class LoggerFilter(logging.Filter):
    COLOR = {
        'DEBUG': 'GREEN',
        'INFO': 'GREEN',
        'WARNING': 'YELLOW',
        'ERROR': 'RED',
        'CRITICAL': 'RED',
    }

    def filter(self, record):
        record.color = LoggerFilter.COLOR[record.levelname]
        return True


class Logger:
    _log_format = '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

    @property
    def file_handler(self) -> logging.FileHandler:
        file_handler = logging.FileHandler(settings.LOGS_FILE)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(self._log_format))
        return file_handler

    @property
    def stream_handler(self) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(self._log_format))
        return stream_handler

    def __call__(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addFilter(LoggerFilter())
        logger.addHandler(self.file_handler)
        logger.addHandler(self.stream_handler)
        return logger


logger = Logger()
