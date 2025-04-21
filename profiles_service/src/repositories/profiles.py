from asyncpg.connection import Connection
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.schemas.profile import CreateProfileSchema, ProfileSchema


class ProfilesRepository(BaseRepository):
    @staticmethod
    async def create(
        connection: Connection,
        table_name: str,
        schema: type[BaseModel],
        create_data: CreateProfileSchema,
    ) -> ProfileSchema:
        return await super(__class__, __class__).create(
            connection,
            'dating.profiles',
            ProfileSchema,
            create_data,
        )


