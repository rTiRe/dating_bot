from typing import Any

from src.specifications.base import Specification


class EqualsSpecification(Specification):
    def __init__(self, attribute: str, value: Any) -> None:
        self.attribute = attribute
        self.value = value

    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} = ??', [self.value]


class NotEqualsSpecification(EqualsSpecification):
    def __init__(self, attribute: str, value: Any) -> None:
        super().__init__(attribute, value)

    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} != ??', [self.value]


class InSpecification(Specification):
    def __init__(self, attribute: str, *values: Any) -> None:
        self.attribute = attribute
        self.values = values

    def to_sql(self):
        if not self.values:
            return '1=0', []
        if len(self.values) == 1:
            return f'{self.column} = ??', self.values
        placeholders = ', '.join('??' * len(self.values))
        return f'{self.attribute} IN ({placeholders})', self.values
