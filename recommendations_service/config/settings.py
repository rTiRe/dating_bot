from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    ELASTICSEARCH_URL: str
    ELASTICSEARCH_USER: str
    ELASTICSEARCH_PASS: SecretStr

    LOGS_FILE: str = 'logs.log'

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings()
