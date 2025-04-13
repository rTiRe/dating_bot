"""Module for manage GRPC connection with accounts service."""

from uuid import UUID

from config import logger, settings
from src.api.grpc.connections.base import BaseConnection
from src.api.grpc.protobufs import accounts_pb2, accounts_pb2_grpc

logger = logger(__name__)


class AccountsConnection(BaseConnection):
    """Account connection class."""

    def __init__(self, url: str):
        """Init.

        Args:
            url (str): GRPC service url.
        """
        super().__init__(url)
        self.__stub = accounts_pb2_grpc.AccountsServiceStub(self.channel)

    @property
    def stub(self) -> accounts_pb2_grpc.AccountsServiceStub:
        """Get service stub.

        Returns:
            accounts_pb2_grpc.AccountsServiceStub: GRPC service stub.
        """
        return self.__stub

    async def get_by_telegram_id(
        self,
        telegram_id: int,
        telegram_username: str | None = None,
    ) -> accounts_pb2.AccountsGetResponse:
        """Send request for get account data by telegram id.

        Args:
            telegram_id (int): account telegram id.
            telegram_username (str | None, optional): account telegram username for update. Defaults to None.

        Returns:
            accounts_pb2.AccountsGetResponse: account data.
        """
        request_data = {'telegram_id': telegram_id}
        if telegram_username is not None:
            request_data['telegram_username'] = telegram_username
        user_request = accounts_pb2.AccountsGetRequest(**request_data)
        return self.stub.Get(user_request)

    async def get_by_id(
        self,
        id: str | UUID,  # noqa: WPS125
        telegram_username: str | None = None,
    ) -> accounts_pb2.AccountsGetResponse:
        """Send request for get account data by id.

        Args:
            id (str | UUID): account id.
            telegram_username (str | None, optional): account telegram username for update. Defaults to None.

        Returns:
            accounts_pb2.AccountsGetResponse: account data.
        """
        if not isinstance(id, UUID):
            id = UUID(id)  # noqa: WPS125
        request_data = {'id': str(id)}
        if telegram_username is not None:
            request_data['telegram_username'] = telegram_username
        user_request = accounts_pb2.AccountsGetRequest(**request_data)
        return self.stub.Get(user_request)

    async def get_or_create(
        self,
        telegram_id: int,
        telegram_username: str | None = None,
    ) -> accounts_pb2.AccountsGetResponse:
        """Send request for get account data or create account and get its data.

        Args:
            telegram_id (int): account telegram id.
            telegram_username (str | None, optional): account telegram username for update. Defaults to None.

        Returns:
            accounts_pb2.AccountsGetResponse: account data.
        """
        request_data = {'telegram_id': telegram_id}
        if telegram_username is not None:
            request_data['telegram_username'] = telegram_username
        user_request = accounts_pb2.AccountsCreateRequest(**request_data)
        return self.stub.GetOrCreate(user_request)


accounts_connection = AccountsConnection(settings.ACCOUNTS_GRPC_URL)
