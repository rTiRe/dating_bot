from abc import ABC, abstractmethod
from typing import Any


class Specification(ABC):
    @staticmethod
    async def to_asyncpg_query(query: str) -> str:
        parts = query.split('??')
        new_query = []
        for num, part in enumerate(parts[:-1]):
            new_query.append(f'{part}${num + 1}')  # noqa: WPS237
        new_query.append(parts[-1])
        return ''.join(new_query)

    @abstractmethod
    async def to_sql(self) -> tuple[str, list[Any]]:
        raise NotImplementedError()

    def __and__(self, other: 'Specification') -> 'AndSpecification':
        return AndSpecification(self, other)

    def __or__(self, other: 'Specification') -> 'OrSpecification':
        return OrSpecification(self, other)

    def __invert__(self) -> 'NotSpecification':
        return NotSpecification(self)

    def __neg__(self) -> 'NotSpecification':
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, *specifications: Specification) -> None:
        self.specifications = specifications

    async def to_sql(self) -> tuple[str, list[Any]]:
        conditions = []
        conditions_params = []
        for specification in self.specifications:
            condition, condition_param = await specification.to_sql()
            conditions.append(condition)
            conditions_params.extend(condition_param)
        return ' and '.join(f'({condition})' for condition in conditions), conditions_params


class OrSpecification(Specification):
    def __init__(self, *specifications: Specification) -> None:
        self.specifications = specifications

    async def to_sql(self) -> tuple[str, list[Any]]:
        conditions = []
        conditions_params = []
        for specification in self.specifications:
            condition, condition_param = await specification.to_sql()
            conditions.append(condition)
            conditions_params.extend(condition_param)
        return ' or '.join(f'({condition})' for condition in conditions), conditions_params


class NotSpecification(Specification):
    def __init__(self, specification: Specification) -> None:
        self.specification = specification

    async def to_sql(self) -> tuple[str, list[Any]]:
        condition, condition_param = await self.specification.to_sql()
        return f'not ({condition})', condition_param
