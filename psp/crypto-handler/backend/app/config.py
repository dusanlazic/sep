from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".develop.env", ".env"), extra="ignore"
    )


config = Config()
