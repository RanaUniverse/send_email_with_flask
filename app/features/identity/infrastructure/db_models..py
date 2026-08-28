"""
app/features/identity/infrastructure/db_models..py

Here i will defines the database models so that
i can use sqlmodel here as my user storage


i need to remove this #TODO
"""

from datetime import datetime


from sqlmodel import SQLModel, Field


class UserModel(
    SQLModel,
    table=True,
):
    id_: int | None = Field(
        default=None,
        primary_key=True,
    )
    first_name: str | None = Field(
        default=None,
        description="This is the First name of user given by user after registraion "
        "if he wants to give his name",
    )
    last_name: str | None = Field(
        default=None,
        description="Last name of the user maybe not given by user will ok ",
    )
    email: str = Field(
        unique=True,
        index=True,
    )
    password_hash: str
    last_login_time: datetime | None = None

    is_active: bool = True
    is_verified: bool = False
