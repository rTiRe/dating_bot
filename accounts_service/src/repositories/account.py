from asyncpg.connection import Connection

from src.schemas import AccountSchema, CreateAccountSchema, UpdateAccountSchema
from src.specifications import Specification
from src.repositories.base import BaseRepository


class AccountRepository(BaseRepository):
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

    async def get(
        connection: Connection,
        *specifications: Specification,
        page: int = 1,
        page_size: int = 100,
    ) -> AccountSchema:
        return await super(__class__, __class__).get(
            connection,
            'dating.accounts',
            AccountSchema,
            *specifications,
            page=page,
            page_size=page_size,
        )

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
