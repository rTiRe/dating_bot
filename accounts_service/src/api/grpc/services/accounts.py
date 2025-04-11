import grpc

from src.api.grpc.protobufs.accounts import accounts_pb2, accounts_pb2_grpc
from src.repositories import AccountRepository
from src.specifications import EqualsSpecification
from src.storage.postgres import database
from src.schemas import AccountSchema, UpdateAccountSchema


class AccountsService(accounts_pb2_grpc.AccountsServiceServicer):
    @staticmethod
    async def serve() -> None:
        server = grpc.aio.server()
        accounts_pb2_grpc.add_AccountsServiceServicer_to_server(AccountsService(), server)
        server.add_insecure_port('[::]:1337')
        await server.start()
        await server.wait_for_termination()

    async def Get(
        self,
        request: accounts_pb2.AccountsGetRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsGetResponse:
        async with database.pool.acquire() as connection:
            specification = EqualsSpecification('telegram_id', request.telegram_id)
            account: AccountSchema = (await AccountRepository.get(connection, specification))[0]
            if request.telegram_username and account.telegram_username != request.telegram_username:
                if request.telegram_username == '0':
                    update_data = UpdateAccountSchema(telegram_username=None)
                else:
                    update_data = UpdateAccountSchema(telegram_username=request.telegram_username)
                await AccountRepository.update(
                    connection,
                    specification,
                    data=update_data,
                )
                setattr(account, 'telegram_username', update_data.telegram_username)
        return accounts_pb2.AccountsGetResponse(
            id=str(account.id),
            telegram_id=account.telegram_id,
            telegram_username=account.telegram_username,
            created_at=account.created_at.isoformat(),
            updated_at=account.updated_at.isoformat(),
        )

