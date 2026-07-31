"""
app/shared/email/models.py

"""

from pydantic import BaseModel, EmailStr, ConfigDict


class SMTPConfig(BaseModel):
    host: str
    port: int


class AuthSMTPConfig(SMTPConfig):
    username: str
    password: str


class EmailMessageData(BaseModel):

    model_config = ConfigDict(
        validate_assignment=True,
    )

    to_email: list[EmailStr]

    subject: str
    body: str

    from_email: EmailStr | None = None
    # if i will not use this upper value it will use from config

    reply_to: EmailStr | None = None
    cc: list[EmailStr] | None = None
    bcc: list[EmailStr] | None = None
