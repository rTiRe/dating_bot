from asyncpg import Record
from asyncpg.connection import Connection
from pydantic import BaseModel

from src.exceptions import UpdateAllRowsException
from src.repositories.base import BaseRepository
from src.schemas.profile import CreateProfileSchema, ProfileSchema, UpdateProfileSchema
from src.specifications.base import Specification


class ProfilesRepository(BaseRepository):
    @staticmethod
    async def create(
        connection: Connection,
        create_data: CreateProfileSchema,
    ) -> ProfileSchema:
        data_dict = create_data.model_dump()
        data_dict['gender'] = str(data_dict['gender'].value)
        statement_values = []
        columns = ', '.join([column for column in data_dict.keys()])
        values_pattern = ', '.join('??' for _ in range(len(data_dict)))
        statement_values.extend(list(data_dict.values()))
        statement = f"""
            insert into dating.profiles ({columns}) values ({values_pattern})
            returning *
        """
        statement = await Specification.to_asyncpg_query(f'{statement};')
        model_data: Record = await connection.fetchrow(statement, *statement_values)
        return ProfileSchema(**model_data)

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
        if not specifications and not update_all:
            raise UpdateAllRowsException(
                f'You are trying to update all rows from a table dating.profiles. '
                'If you are sure, set update_all to True.'
            )
        update_values = update_data.model_dump(exclude_unset=True)
        if update_values.get('gender'):
            update_values['gender'] = str(update_values['gender'].value)
        set_statement = ', '.join([f'{column} = ??' for column in update_values.keys()])
        statement_values = list(update_values.values())
        statement = f'update dating.profiles set {set_statement}'
        if specifications:
            statement, statement_values = await BaseRepository.add_conditions(
                statement,
                statement_values,
                *specifications,
            )
        statement = await Specification.to_asyncpg_query(f'{statement};')
        return await connection.execute(statement, *statement_values)

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