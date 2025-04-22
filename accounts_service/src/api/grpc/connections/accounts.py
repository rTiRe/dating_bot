from uuid import UUID

from src.api.grpc.connections.base import BaseConnection
from src.api.grpc.protobufs.accounts import accounts_pb2, accounts_pb2_grpc
from config import settings, logger


logger = logger(__name__)


class AccountsConnection(BaseConnection):
    def __init__(self, url: str):
        host, port = url.split(':', maxsplit=1)
        try:
            int(port)
        except ValueError:
            error_text = 'Account GRPC URL port must be an integer'
            logger.error(error_text)
            raise ValueError(error_text)
        super().__init__(host, port)
        self.__stub = accounts_pb2_grpc.AccountsServiceStub(self.channel)

    @property
    def stub(self) -> accounts_pb2_grpc.AccountsServiceStub:
        return self.__stub

    async def get_by_telegram_id(
        self,
        telegram_id: int,
        telegram_username: str | None = None
    ) -> accounts_pb2.AccountsGetResponse:
        request_data = {'telegram_id': telegram_id}
        if telegram_username is not None:
            request_data['telegram_username'] = telegram_username
        user_request = accounts_pb2.AccountsGetRequest(**request_data)
        return self.stub.Get(user_request)

    async def get_by_id(
        self,
        id: str | UUID,
        telegram_username: str | None = None
    ) -> accounts_pb2.AccountsGetResponse:
        if not isinstance(id, UUID):
            id = UUID(id)
        request_data = {'id': str(id)}
        if telegram_username is not None:
            request_data['telegram_username'] = telegram_username
        user_request = accounts_pb2.AccountsGetRequest(**request_data)
        return self.stub.Get(user_request)


# accounts_connection = AccountsConnection(settings.ACCOUNTS_GRPC_URL)
