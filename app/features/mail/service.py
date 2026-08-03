"""
app/features/mail/service.py

Here i will keep the business logic of what to do
or what to validate or not i will call the operations.py
"""

from pydantic import EmailStr


from app.shared.mail.models import EmailMessageData

from app.shared.mail.sender import EmailSender
from app.shared.mail.factory import mail_sender


from app.shared.security.otp_generate import generate_otp
from app.shared.security.otp_templates import otp_email_body


class MailService:
    def __init__(
        self,
        sender: EmailSender,
    ) -> None:
        self.sender = sender

    def send_otp(
        self,
        to_email: EmailStr,
    ):
        # this otp generate will be done in another fun

        msg_body = otp_email_body(
            otp=generate_otp(),
            valid_seconds=100,
        )

        mail_data = EmailMessageData(
            to_email=[to_email],
            subject="Verify Your OTP- Rana Universe",
            body=msg_body,
        )
        self.sender.send_mail(
            email_msg=mail_data,
        )


def send_otp_to_email(to_email: str):
    m = MailService(
        sender=mail_sender,
    )
    m.send_otp(
        to_email=to_email,
    )


def send_email_to_one_user():
    """
    This will just Send the mail to the user or whatsoever
    This is my business logic,
    here it will choose if the mail will go over gmail, local or anything else
    """
    pass
