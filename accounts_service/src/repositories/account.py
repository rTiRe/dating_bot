from asyncpg.connection import Connection

from src.schemas import AccountSchema, CreateAccountSchema, UpdateAccountSchema
from src.specifications import Specification, EqualsSpecification
from src.repositories.base import BaseRepository
from src.storage.postgres import database


class AccountRepository(BaseRepository):
    @staticmethod
    async def create(
        connection: Connection,
        data: CreateAccountSchema,
    ) -> AccountSchema:
        return await super(__class__, __class__).create(
            connection,
            'dating.accounts',
            AccountSchema,
            data,
        )

    @staticmethod
    async def get(
        connection: Connection,
        *specifications: Specification,
        page: int = 1,
        page_size: int = 100,
    ) -> list[AccountSchema]:
        return await super(__class__, __class__).get(
            connection,
            'dating.accounts',
            AccountSchema,
            *specifications,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    async def update(
        connection: Connection,
        *specifications: Specification,
        update_all: bool = False,
        data: UpdateAccountSchema,
    ) -> str:
        return await super(__class__, __class__).update(
            connection,
            'dating.accounts',
            *specifications,
            update_all=update_all,
            data=data,
        )

    @staticmethod
    async def delete(
        connection: Connection,
        *specifications: Specification,
        delete_all: bool = False,
    ) -> str:
        return await super(__class__, __class__).delete(
            connection,
            'dating.accounts',
            *specifications,
            delete_all=delete_all,
        )

    @staticmethod
    async def get_or_create(
        connection: Connection,
        data: CreateAccountSchema,
    ) -> AccountSchema:
        specification = EqualsSpecification('telegram_id', data.telegram_id)
        accounts = await AccountRepository.get(connection, specification)
        if len(accounts):
            return accounts[0]
        return await AccountRepository.create(connection, data)
