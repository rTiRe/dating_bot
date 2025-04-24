from datetime import datetime
from enum import Enum
from typing import Self, Annotated
from uuid import UUID

from pydantic import BaseModel, model_validator, field_validator, AfterValidator

from src.api.grpc.protobufs.profiles.profiles_pb2 import Gender


class GenderEnum(Enum):
    GENDER_DEFAULT = Gender.GENDER_DEFAULT
    GENDER_MALE = Gender.GENDER_MALE
    GENDER_FEMALE = Gender.GENDER_FEMALE


def check_gender(gender: GenderEnum | int) -> GenderEnum:
    if isinstance(gender, GenderEnum):
        return gender
    return GenderEnum(gender)


class ProfileSchema(BaseModel):
    id: UUID
    account_id: UUID
    first_name: str
    last_name: str
    age: int
    gender: Annotated[GenderEnum | int, AfterValidator(check_gender)]
    biography: str | None = None
    language_locale: str
    created_at: datetime
    updated_at: datetime
    image_names: list[str]
    lat: float
    lon: float


class CreateProfileSchema(BaseModel):
    account_id: UUID
    first_name: str
    last_name: str
    age: int
    gender: Annotated[GenderEnum | int, AfterValidator(check_gender)]
    biography: str | None = None
    language_locale: str
    lat: float
    lon: float


class UpdateProfileSchema(BaseModel):
    account_id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: Annotated[GenderEnum | int, AfterValidator(check_gender)] | None = None
    biography: str | None = None
    language_locale: str | None = None
    image_base64_list: list[str] | None = None
    lat: float | None = None
    lon: float | None = None
