from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class GenderEnum(Enum):
    GENDER_MALE = 0
    GENDER_FEMALE = 1


class ProfileSchema(BaseModel):
    id: UUID
    account_id: UUID
    first_name: str
    last_name: str
    age: int
    gender: GenderEnum
    biography: str | None = None
    additional_info: str | None = None
    created_at: datetime
    updated_at: datetime


class CreateProfileSchema(BaseModel):
    account_id: UUID
    first_name: str
    last_name: str
    age: int
    gender: GenderEnum
    biography: str | None = None
    additional_info: str | None = None


class UpdateProfileSchema(BaseModel):
    account_id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None
    biography: str | None = None
    additional_info: str | None = None
