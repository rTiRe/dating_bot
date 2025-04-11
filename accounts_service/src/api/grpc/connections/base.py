from abc import ABC
from typing import Any

from grpc import Channel, insecure_channel


class BaseConnection(ABC):
    def __check_type(self, name: str, value: Any, types: tuple[type]):
        types = tuple(types)
        if not isinstance(value, types):
            types_string = ', '.join(types)
            raise TypeError(f'"{name}" must be {types_string}, not {type(value).__name__}')

    def __init__(self, host: str, port: int) -> None:
        self.__check_type('host', host, (str,))
        self.__check_type('port', port, (int,))
        self.__channel = insecure_channel(f'{host}:{port}')

    @property
    def channel(self) -> Channel:
        return self.__channel
