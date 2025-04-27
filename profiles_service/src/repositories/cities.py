from asyncpg import Connection

from src.repositories.base import BaseRepository
from src.schemas.city import CitySchema, UpdateCitySchema, CreateCitySchema
from src.specifications.base import Specification


class CitiesRepository(BaseRepository):
    @staticmethod
    async def create(
            connection: Connection,
            create_data: CreateCitySchema,
    ) -> CitySchema:
        return await super(__class__, __class__).create(
            connection,
            'dating.cities',
            CitySchema,
            create_data,
        )

    @staticmethod
    async def get(
        connection: Connection,
        *specifications: Specification,
        page: int = 1,
        page_size: int = 100,
    ) -> list[CitySchema]:
        return await super(__class__, __class__).get(
            connection,
            'dating.cities',
            CitySchema,
            *specifications,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    async def update(
        connection: Connection,
        *specifications: Specification,
        update_all: bool = False,
        update_data: UpdateCitySchema,
    ) -> str:
        return await super(__class__, __class__).update(
            connection,
            'dating.cities',
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
            'dating.cities',
            *specifications,
            delete_all=delete_all,
        )
