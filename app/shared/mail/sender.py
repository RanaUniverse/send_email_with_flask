"""
app/shared/mail/sender.py


"""

import smtplib
import ssl

from typing import Protocol
from pydantic import EmailStr

from .models import (
    SMTPConfig,
    AuthSMTPConfig,
    EmailMessageData,
)
from .email_builder import build_email_message


class EmailSender(Protocol):
    def send_mail(
        self,
        email_msg: EmailMessageData,
    ) -> None:
        pass


class LocalMailSender:
    def __init__(
        self,
        mail_config: SMTPConfig,
        default_from: EmailStr,
    ) -> None:
        self.config = mail_config
        self.default_from = default_from

    def send_mail(
        self,
        email_msg: EmailMessageData,
    ) -> None:
        msg = build_email_message(
            email_msg=email_msg,
            default_from_email=self.default_from,
        )
        with smtplib.SMTP(
            host=self.config.host,
            port=self.config.port,
        ) as server:
            server.send_message(
                msg=msg,
            )


class AuthenticatedSMTPSender:

    def __init__(
        self,
        mail_config: AuthSMTPConfig,
        default_from: EmailStr,
    ) -> None:
        self.config = mail_config
        self.default_from = default_from

    def send_mail(
        self,
        email_msg: EmailMessageData,
    ):
        msg = build_email_message(
            email_msg=email_msg,
            default_from_email=self.default_from,
        )
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            host=self.config.host,
            port=self.config.port,
            context=context,
        ) as server:
            server.login(
                user=self.config.username,
                password=self.config.password,
            )
            server.send_message(
                msg=msg,
            )
