from abc import ABC, abstractmethod
from typing import Any

from asyncpg import Record
from asyncpg.connection import Connection
from pydantic import BaseModel

from src.exceptions import DeleteAllRowsException, UpdateAllRowsException
from src.specifications import AndSpecification, Specification


class BaseRepository(ABC):
    @staticmethod
    async def add_conditions(
        statement: str,
        statement_values: list[Any],
        *specifications: Specification,
    ) -> tuple[str, list[Any]]:
        combined_specifications = AndSpecification(*specifications)
        where_statement, where_values = await combined_specifications.to_sql()
        statement = f'{statement} where {where_statement}'
        statement_values.extend(where_values)
        return statement, statement_values

    @staticmethod
    @abstractmethod
    async def create(
        connection: Connection,
        table_name: str,
        schema: type[BaseModel],
        create_data: BaseModel,
    ) -> BaseModel:
        data_dict = create_data.model_dump()
        statement_values = []
        columns = ', '.join([column for column in data_dict.keys()])
        values_pattern = ', '.join('??' for _ in range(len(data_dict)))
        statement_values.extend(list(data_dict.values()))
        statement = f"""
            insert into {table_name} ({columns}) values ({values_pattern})
            returning *
        """
        statement = await Specification.to_asyncpg_query(f'{statement};')
        model_data: Record = await connection.fetchrow(statement, *statement_values)
        return schema(**model_data)

    @staticmethod
    @abstractmethod
    async def get(
        connection: Connection,
        table_name: str,
        schema: type[BaseModel],
        *specifications: Specification,
        page: int = 1,
        page_size: int = 100,
    ) -> list[BaseModel]:
        statement_values = []
        statement = f'select * from {table_name}'
        if specifications:
            statement, statement_values = await BaseRepository.add_conditions(
                statement,
                statement_values,
                *specifications,
            )
        offset = page_size * (page - 1)
        statement = f'{statement} limit {page_size} offset {offset}'
        statement = await Specification.to_asyncpg_query(f'{statement};')
        models_data: list[Record] = await connection.fetch(statement, *statement_values)
        return [schema(**model_data) for model_data in models_data]

    @staticmethod
    @abstractmethod
    async def update(
        connection: Connection,
        table_name: str,
        *specifications: Specification,
        update_all: bool = False,
        update_data: BaseModel,
    ) -> str:
        if not specifications and not update_all:
            raise UpdateAllRowsException(
                f'You are trying to update all rows from a table {table_name}. '
                'If you are sure, set update_all to True.'
            )
        update_values = update_data.model_dump(exclude_unset=True)
        set_statement = ', '.join([f'{column} = ??' for column in update_values.keys()])
        statement_values = list(update_values.values())
        statement = f'update {table_name} set {set_statement}'
        if specifications:
            statement, statement_values = await BaseRepository.add_conditions(
                statement,
                statement_values,
                *specifications,
            )
        statement = await Specification.to_asyncpg_query(f'{statement};')
        return await connection.execute(statement, *statement_values)

    @staticmethod
    @abstractmethod
    async def delete(
        connection: Connection,
        table_name: str,
        *specifications: Specification,
        delete_all: bool = False,
    ) -> str:
        if not specifications and not delete_all:
            raise DeleteAllRowsException(
                f'You are trying to delete all rows from a table {table_name}. '
                'If you are sure, set delete_all to True.'
            )
        statement_values = []
        statement = f'delete from {table_name}'
        if specifications:
            statement, statement_values = await BaseRepository.add_conditions(
                statement,
                statement_values,
                *specifications,
            )
        statement = await Specification.to_asyncpg_query(f'{statement};')
        return await connection.execute(statement, *statement_values)
