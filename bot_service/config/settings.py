from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    RABBITMQ_URL: str
    ACCOUNTS_GRPC_URL: str

    LOGS_FILE: str = 'logs.log'

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
