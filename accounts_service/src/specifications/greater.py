from typing import Any

from src.specifications.base import Specification


class GreaterThanSpecification(Specification):
    def __init__(self, attribute: str, compare_value: Any) -> None:
        self.attribute = attribute
        self.compare_value = compare_value

    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} > ??', [self.compare_value]


class GreaterEqualsSpecification(GreaterThanSpecification):
    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} >= ??', [self.compare_value]
