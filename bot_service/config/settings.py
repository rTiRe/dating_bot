"""Module for manage app settings."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings."""

    BOT_TOKEN: SecretStr
    RABBITMQ_URL: str
    REDIS_URL: str
    REDIS_FSM_URL: str
    ACCOUNTS_GRPC_URL: str
    PROFILES_GRPC_URL: str
    RECOMMENDATIONS_GRPC_URL: str

    LOGS_FILE: str = 'logs.log'

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
