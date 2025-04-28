from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import SecretStr # type: ignore


class Settings(BaseSettings):
    ELASTICSEARCH_URL: str
    ELASTICSEARCH_USER: str
    ELASTICSEARCH_PASS: SecretStr

    LOGS_FILE: str = 'logs.log'

    model_config = SettingsConfigDict(
        env_file='config/.env',
        extra='ignore',
    )


settings = Settings() # type: ignore
