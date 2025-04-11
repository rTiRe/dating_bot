from src.api.grpc.connections.base import BaseConnection

from src.api.grpc.protobufs.accounts.accounts_pb2_grpc import AccountsServiceStub
from src.api.grpc.protobufs.accounts.accounts_pb2 import GetRequest, GetResponse
from config import settings


class AccountsConnection(BaseConnection):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.__stub = AccountsServiceStub(self.channel)

    @property
    def stub(self) -> AccountsServiceStub:
        return self.__stub


# accounts_connection = AccountsConnection(
#     host=settings.USERS_GRPC_HOST,
#     port=settings.USERS_GRPC_PORT,
# )
