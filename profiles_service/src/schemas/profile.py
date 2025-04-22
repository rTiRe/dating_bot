from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.api.grpc.protobufs.profiles.profiles_pb2 import Gender


class ProfileSchema(BaseModel):
    id: UUID
    account_id: UUID
    first_name: str
    last_name: str
    age: int
    gender: Gender
    biography: str | None = None
    additional_info: str | None = None
    language: str
    created_at: datetime
    updated_at: datetime


class CreateProfileSchema(BaseModel):
    account_id: UUID
    first_name: str
    last_name: str
    age: int
    gender: Gender
    biography: str | None = None
    additional_info: str | None = None
    language: str


class UpdateProfileSchema(BaseModel):
    account_id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    gender: Gender | None = None
    biography: str | None = None
    additional_info: str | None = None
    language: str
