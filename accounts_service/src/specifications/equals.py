from typing import Any

from src.specifications.base import Specification


class EqualsSpecification(Specification):
    def __init__(self, attribute: str, compare_value: Any) -> None:
        self.attribute = attribute
        self.compare_value = compare_value

    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} = ??', [self.compare_value]


class NotEqualsSpecification(EqualsSpecification):
    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} != ??', [self.compare_value]


class InSpecification(Specification):
    def __init__(self, attribute: str, *compare_values: Any) -> None:
        self.attribute = attribute
        self.compare_values = compare_values

    def to_sql(self):
        if not self.compare_values:
            return '1=0', []
        if len(self.compare_values) == 1:
            return f'{self.column} = ??', self.compare_values
        placeholders = ', '.join('??' * len(self.compare_values))
        return f'{self.attribute} IN ({placeholders})', self.compare_values
