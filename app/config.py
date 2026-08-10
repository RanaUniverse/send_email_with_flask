"""
app/config.py

This will be store the configuration settings here
"""

from functools import lru_cache
from typing import Literal

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
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

    validation_mode: Literal[
        "DEVELOPMENT",
        "PRODUCTION",
    ]


class MailAddressSettings(BaseModel):
    """
    All the email address which need to be given
    in different case i will keep those here
    """

    from_email_default: EmailStr

    reply_to_default: EmailStr | None = Field(default=None, repr=False)
    reply_to_billing: EmailStr | None = Field(default=None, repr=False)
    reply_to_otp: EmailStr | None = Field(default=None, repr=False)
    reply_to_support: EmailStr | None = Field(default=None, repr=False)
    reply_to_sales: EmailStr | None = Field(default=None, repr=False)
    reply_to_security: EmailStr | None = Field(default=None, repr=False)
    reply_to_account: EmailStr | None = Field(default=None, repr=False)
    reply_to_jobs: EmailStr | None = Field(default=None, repr=False)
    reply_to_login: EmailStr | None = Field(default=None, repr=False)
    reply_to_welcome: EmailStr | None = Field(default=None, repr=False)


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
    security: Literal[
        "ssl",
        "starttls",
    ]

    address: MailAddressSettings


class Settings(BaseSettings):
    owner_name: str

    app: AppSettings
    mail: MailSettings = Field(repr=False)

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
