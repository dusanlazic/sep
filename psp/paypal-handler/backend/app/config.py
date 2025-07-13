from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    paypal_client_id: str
    paypal_client_secret: str
    paypal_api_base: HttpUrl
    psp_api_base_url: HttpUrl

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".develop.env", ".env"), extra="ignore"
    )


config = Config()
