from asyncpg.connection import Connection
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.schemas.profile import CreateProfileSchema, ProfileSchema, UpdateProfileSchema
from src.specifications.base import Specification


class ProfilesRepository(BaseRepository):
    @staticmethod
    async def create(
        connection: Connection,
        create_data: CreateProfileSchema,
    ) -> ProfileSchema:
        return await super(__class__, __class__).create(
            connection,
            'dating.profiles',
            ProfileSchema,
            create_data,
        )

    @staticmethod
    async def get(
        connection: Connection,
        *specifications: Specification,
        page: int = 1,
        page_size: int = 100,
    ) -> list[ProfileSchema]:
        return await super(__class__, __class__).get(
            connection,
            'dating.profiles',
            ProfileSchema,
            *specifications,
            page=page,
            page_size=page_size
        )

    @staticmethod
    async def update(
            connection: Connection,
            *specifications: Specification,
            update_all: bool = False,
            update_data: UpdateProfileSchema,
    ) -> str:
        return await super(__class__, __class__).update(
            connection,
            'dating.profiles',
            *specifications,
            update_all=update_all,
            update_data=update_data,
        )

    @staticmethod
    async def delete(
        connection: Connection,
        *specifications: Specification,
        delete_all: bool = False,
    ) -> str:
        return await super(__class__, __class__).delete(
            connection,
            'dating.profiles',
            *specifications,
            delete_all=delete_all,
        )