from uuid import UUID

import grpc
from asyncpg.exceptions import UniqueViolationError

from config import logger
from src.api.grpc.protobufs import accounts_pb2, accounts_pb2_grpc
from src.repositories import AccountsRepository
from src.schemas import CreateAccountSchema, UpdateAccountSchema
from src.specifications import EqualsSpecification
from src.storage.postgres import database

logger = logger(__name__)


class AccountsService(accounts_pb2_grpc.AccountsServiceServicer):  # noqa: WPS214, WPS338
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

    @staticmethod
    async def __check_telegram_username(telegram_username: str) -> None:
        min_username_length = 4
        max_username_length = 32
        if telegram_username and not (min_username_length <= len(telegram_username) <= max_username_length):
            raise ValueError(
                'The length of the telegram_username field value must be from 4 to 32 characters',
            )

    name_to_checker = {
        'id': __check_id,
        'telegram_id': __check_telegram_id,
        'telegram_username': __check_telegram_username,
    }

    async def Create(
        self,
        request: accounts_pb2.AccountsCreateRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsCreateResponse:
        try:  # noqa: WPS229
            await self.__check_telegram_id(request.telegram_id)
            await self.__check_telegram_username(request.telegram_username)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        create_schema = CreateAccountSchema(
            telegram_id=request.telegram_id,
            telegram_username=request.telegram_username,
        )
        async with database.pool.acquire() as connection:
            try:
                account = await AccountsRepository.create(connection, create_schema)
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
        try:
            await self.name_to_checker[identifier_field](getattr(request, identifier_field))
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification(identifier_field, getattr(request, identifier_field))
        async with database.pool.acquire() as connection:
            accounts = (await AccountsRepository.get(connection, specification))
            if len(accounts) == 0:
                await context.abort(grpc.StatusCode.NOT_FOUND)
            account = accounts[0]
            is_username_setted = request.HasField('telegram_username')
            if is_username_setted and account.telegram_username != request.telegram_username:
                try:
                    await self.__check_telegram_username(request.telegram_username)
                except ValueError as exception:
                    await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
                update_data = UpdateAccountSchema(telegram_username=request.telegram_username)
                await AccountsRepository.update(connection, specification, update_data=update_data)
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
        update_data = {descriptor.name: field_value for descriptor, field_value in request.data.ListFields()}
        if not update_data:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'Empty update data')
        for name, field_value in update_data.items():
            try:  # noqa: WPS229
                await self.__check_id(request.id)
                await self.name_to_checker[name](field_value)
            except ValueError as exception:
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification('id', request.id)
        update_schema = UpdateAccountSchema(**update_data)
        async with database.pool.acquire() as connection:
            try:
                update_result = await AccountsRepository.update(
                    connection,
                    specification,
                    update_data=update_schema,
                )
            except UniqueViolationError as exception:
                logger.error(exception)
                await context.abort(
                    grpc.StatusCode.ALREADY_EXISTS,
                    'An account with this telegram_id field already exists',
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
            delete_result = await AccountsRepository.delete(connection, delete_specification)
        return accounts_pb2.AccountsDeleteResponse(result=delete_result)

    async def GetOrCreate(
        self,
        request: accounts_pb2.AccountsCreateRequest,
        context: grpc.aio.ServicerContext,
    ) -> accounts_pb2.AccountsGetResponse:
        try:  # noqa: WPS229
            await self.__check_telegram_id(request.telegram_id)
            await self.__check_telegram_username(request.telegram_username)
        except ValueError as exception:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exception))
        specification = EqualsSpecification('telegram_id', request.telegram_id)
        is_username_setted = request.HasField('telegram_username')
        create_schema = CreateAccountSchema(
            telegram_id=request.telegram_id,
            telegram_username=request.telegram_username,
        )
        async with database.pool.acquire() as connection:
            try:
                account = await AccountsRepository.get_or_create(connection, create_schema)
            except Exception as exception:
                logger.error(exception)
                await context.abort(grpc.StatusCode.INTERNAL)
            if is_username_setted and account.telegram_username != request.telegram_username:
                update_data = UpdateAccountSchema(telegram_username=request.telegram_username)
                await AccountsRepository.update(connection, specification, update_data=update_data)
                setattr(account, 'telegram_username', update_data.telegram_username)
        return accounts_pb2.AccountsGetResponse(
            id=str(account.id),
            telegram_id=account.telegram_id,
            telegram_username=account.telegram_username,
            created_at=account.created_at.isoformat(),
            updated_at=account.updated_at.isoformat(),
        )
