from typing import Any

from src.specifications.base import Specification


class LessThanSpecification(Specification):
    def __init__(self, attribute: str, value: Any) -> None:
        self.attribute = attribute
        self.value = value

    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} < ??', [self.value]


class LessEqualsSpecification(LessThanSpecification):
    def __init__(self, attribute: str, value: Any) -> None:
        super().__init__(attribute, value)

    async def to_sql(self) -> tuple[str, list[Any]]:
        return f'{self.attribute} <= ??', [self.value]
