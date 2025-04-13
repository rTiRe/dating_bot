"""Module with abstract connection class."""

from abc import ABC

from grpc import Channel, insecure_channel

from config import logger

logger = logger(__name__)


class BaseConnection(ABC):
    """Abstract connection class."""

    def __init__(self, url: str) -> None:
        """Init.

        Args:
            url (str): channel url.

        Raises:
            Exception: error when creating channel.
        """
        try:
            self.__channel = insecure_channel(url)
        except Exception as exception:
            logger.error(str(exception))
            raise exception

    @property
    def channel(self) -> Channel:
        """Get GRPC connection channel instance.

        Returns:
            Channel: GRPC connection channel instance.
        """
        return self.__channel
