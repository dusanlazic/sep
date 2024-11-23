from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    psp_api_key: str
    jwt_secret: str
    psp_api_base_url: str
    frontend_origin: str

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".develop.env", ".env"), extra="ignore"
    )


config = Config()
