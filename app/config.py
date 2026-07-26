"""
app/config.py

This will be store the configuration settings here
"""

from functools import lru_cache


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
    secret_key: SecretStr


class MailSettings(BaseModel):
    """
    Email related configuraiton will be here
    username and password i will get to login
    and from email is my email id other will see
    """

    host: str
    port: int
    username: str
    password: SecretStr
    from_email: EmailStr


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
