from uuid import UUID

from pydantic import BaseModel


class CitySchema(BaseModel):
    id: UUID
    lat: float
    lon: float


class CreateCitySchema(BaseModel):
    lat: float
    lon: float


class UpdateCitySchema(BaseModel):
    lat: float | None = None
    lon: float | None = None