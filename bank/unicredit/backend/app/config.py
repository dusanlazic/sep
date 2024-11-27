from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    frontend_host: str
    pcc_api_base_url: str = "http://pcc-backend:9000/"
    psp_api_base_url: str = "http://psp-core-backend:9000/"

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".develop.env", ".env"), extra="ignore"
    )


config = Config()
