"""
app/features/mail/service.py

Here i will keep the business logic of what to do
or what to validate or not i will call the operations.py
"""

from pydantic import EmailStr


from app.shared.email.models import EmailMessageData

from app.shared.email.sender import EmailSender
from app.shared.email.factory import mail_sender


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
        random_otp = 123456
        msg_body = (
            f"Hello User, your otp for veification is: {random_otp}, "
            "valid for 60 seconds."
        )

        mail_data = EmailMessageData(
            to_email=[to_email, "x@co.m"],
            subject="OTP SENDING",
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
