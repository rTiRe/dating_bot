from abc import ABC

from grpc import Channel, insecure_channel

from config import logger


logger = logger(__name__)


class BaseConnection(ABC):
    def __init__(self, url: str) -> None:
        try:
            self.__channel = insecure_channel(url)
        except Exception as exception:
            logger.error(str(exception))
            raise exception

    @property
    def channel(self) -> Channel:
        return self.__channel
