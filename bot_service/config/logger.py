"""Module for manage logging."""

import logging

from config.settings import settings


class LoggerFilter(logging.Filter):
    """Class for store logging filters."""

    COLOR = {
        'DEBUG': 'GREEN',
        'INFO': 'GREEN',
        'WARNING': 'YELLOW',
        'ERROR': 'RED',
        'CRITICAL': 'RED',
    }

    def filter(self, record: logging.LogRecord) -> bool:
        """Apply logging filters for record.

        Args:
            record (logging.LogRecord): record for apply filters.

        Returns:
            bool: is filters applied.
        """
        record.color = LoggerFilter.COLOR[record.levelname]
        return True


class Logger:
    """Main logger class."""

    _log_format = '%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

    @property
    def file_handler(self) -> logging.FileHandler:
        """Set up and get file handler.

        Returns:
            logging.FileHandler: setuped file handler.
        """
        file_handler = logging.FileHandler(settings.LOGS_FILE)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(self._log_format))
        return file_handler

    @property
    def stream_handler(self) -> logging.StreamHandler:
        """Set up and get logging stream handler.

        Returns:
            logging.StreamHandler: setuped stream handler.
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(self._log_format))
        return stream_handler

    def __call__(self, name: str) -> logging.Logger:
        """Set up and get logger.

        Args:
            name (str): logger name.

        Returns:
            logging.Logger: named logger.
        """
        module_logger = logging.getLogger(name)
        module_logger.setLevel(logging.INFO)
        module_logger.addFilter(LoggerFilter())
        module_logger.addHandler(self.file_handler)
        module_logger.addHandler(self.stream_handler)
        return module_logger


logger = Logger()
