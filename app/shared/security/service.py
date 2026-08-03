"""
app/shared/security/service.py

I will make different type of service of email
like send otp, welcome and so on
"""

from pydantic import EmailStr

from app.shared.mail.models import EmailMessageData

from app.shared.mail.sender import EmailSender

from app.shared.security.otp_generate import OTPGenerator

from app.shared.security.otp_templates import otp_email_body


class OTPService:

    def __init__(
        self,
        sender: EmailSender,
        generator: OTPGenerator,
    ) -> None:
        self.sender = sender
        self.generator = generator

    def send_otp(
        self,
        email_to: EmailStr,
    ):
        otp = self.generator.generate(
            length=6,
        )

        body = otp_email_body(
            otp=otp,
            valid_seconds=100,
        )

        msg = EmailMessageData(
            to_email=[
                email_to,
            ],
            subject="Vefify Your OTP",
            body=body,
        )

        self.sender.send_mail(
            email_msg=msg,
        )
