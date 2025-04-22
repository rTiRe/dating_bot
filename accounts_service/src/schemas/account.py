from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: UUID
    telegram_id: int
    telegram_username: str | None = None
    created_at: datetime
    updated_at: datetime


class CreateAccountSchema(BaseModel):
    telegram_id: int
    telegram_username: str | None = None


class UpdateAccountSchema(BaseModel):
    telegram_id: int | None = None
    telegram_username: str | None = None
