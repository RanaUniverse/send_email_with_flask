"""
app/config.py

This will be store the configuration settings here
"""

from functools import lru_cache
from typing import Literal

from pydantic import (
    BaseModel,
    EmailStr,
    # Field,
    SecretStr,
)

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppSettings(BaseModel):
    """
    Here i will keep flask app related things to run
    """

    host: str = "0.0.0.0"
    port: int = 9999
    debug: bool = False
    secret_key: SecretStr


class MailSettings(BaseModel):
    """
    Email related configuraiton will be here
    username and password i will get to login
    and from email is my email id other will see
    """

    provider: Literal["local", "smtp"]
    # how i can say it value wil lonly, "local" or "smtp"

    host: str
    port: int
    username: str
    password: SecretStr
    from_email_default: EmailStr
    security: Literal[
        "ssl",
        "starttls",
    ]

    reply_to_default: EmailStr | None = None
    reply_to_billing: EmailStr | None = None
    reply_to_otp: EmailStr | None = None
    reply_to_support: EmailStr | None = None
    reply_to_sales: EmailStr | None = None
    reply_to_security: EmailStr | None = None
    reply_to_account: EmailStr | None = None
    reply_to_jobs: EmailStr | None = None
    reply_to_login: EmailStr | None = None
    reply_to_welcome: EmailStr | None = None


class Settings(BaseSettings):
    owner_name: str

    app: AppSettings
    mail: MailSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow",
    )


@lru_cache
def get_settings() -> Settings:
    """
    i will use this to get my values
    """
    return Settings()  # type: ignore


settings = get_settings()
