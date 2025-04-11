from uuid import UUID

from asyncpg.exceptions import UniqueViolationError
import grpc

from src.api.grpc.protobufs.accounts import accounts_pb2, accounts_pb2_grpc
from src.repositories import AccountRepository
from src.specifications import EqualsSpecification
from src.storage.postgres import database
from src.schemas import AccountSchema, UpdateAccountSchema, CreateAccountSchema


class AccountsService(accounts_pb2_grpc.AccountsServiceServicer):
    @staticmethod
    async def serve() -> None:
        server = grpc.aio.server()
        accounts_pb2_grpc.add_AccountsServiceServicer_to_server(AccountsService(), server)
        server.add_insecure_port('[::]:1337')
        await server.start()
        await server.wait_for_termination()

    @staticmethod
    async def __check_telegram_id(telegram_id: int) -> None:
        if not telegram_id:
            raise ValueError('The telegram_id field must be greater than 0')

    @staticmethod
    async def __check_id(id: str | UUID) -> None:
        if not id:
            raise ValueError('The id field must be set')
        try:
            UUID(id)
        except ValueError:
            raise ValueError('The id field must be of type UUID')

    async def Create(
        self,
        request: accounts_pb2.AccountsCreateRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsCreateResponse:
        try:
            await self.__check_telegram_id(request.telegram_id)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        create_schema = CreateAccountSchema(
            telegram_id=request.telegram_id,
            telegram_username=request.telegram_username,
        )
        async with database.pool.acquire() as connection:
            try:
                account: AccountSchema = await AccountRepository.create(connection, create_schema)
            except UniqueViolationError:
                await context.abort(grpc.StatusCode.ALREADY_EXISTS)
        return accounts_pb2.AccountsCreateResponse(
            id=str(account.id),
            telegram_id=account.telegram_id,
            telegram_username=account.telegram_username,
            created_at=account.created_at.isoformat(),
            updated_at=account.updated_at.isoformat(),
        )

    async def Get(
        self,
        request: accounts_pb2.AccountsGetRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsGetResponse:
        identifier_field = request.WhichOneof('identifier')
        if not identifier_field:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                'The id or telegram_id field must be present',
            )
        check_method = self.__check_id if identifier_field == 'id' else self.__check_telegram_id
        try:
            await check_method(getattr(request, identifier_field))
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification(identifier_field, getattr(request, identifier_field))
        async with database.pool.acquire() as connection:
            accounts: list[AccountSchema] = (await AccountRepository.get(connection, specification))
            if len(accounts) == 0:
                await context.abort(grpc.StatusCode.NOT_FOUND)
            account = accounts[0]
            is_username_setted = request.HasField('telegram_username')
            if is_username_setted and account.telegram_username != request.telegram_username:
                update_data = UpdateAccountSchema(telegram_username=request.telegram_username)
                await AccountRepository.update(connection, specification, data=update_data)
                setattr(account, 'telegram_username', update_data.telegram_username)
        return accounts_pb2.AccountsGetResponse(
            id=str(account.id),
            telegram_id=account.telegram_id,
            telegram_username=account.telegram_username,
            created_at=account.created_at.isoformat(),
            updated_at=account.updated_at.isoformat(),
        )

    async def Update(
        self,
        request: accounts_pb2.AccountsUpdateRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsUpdateResponse:
        try:
            await self.__check_id(request.id)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        update_data = {descriptor.name: value for descriptor, value in request.data.ListFields()}
        if not update_data:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Empty update data')
        async with database.pool.acquire() as connection:
            update_result: str = await AccountRepository.update(
                connection,
                EqualsSpecification('id', request.id),
                data=UpdateAccountSchema(**update_data),
            )
        return accounts_pb2.AccountsUpdateResponse(result=update_result)

    async def Delete(
        self,
        request: accounts_pb2.AccountsDeleteRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsDeleteResponse:
        try:
            await self.__check_id(request.id)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        delete_specification = EqualsSpecification('id', request.id)
        async with database.pool.acquire() as connection:
            delete_result: str = await AccountRepository.delete(connection, delete_specification)
        return accounts_pb2.AccountsDeleteResponse(result=delete_result)
