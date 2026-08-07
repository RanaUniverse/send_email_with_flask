"""
app/shared/otp/send.py

This is for send otp to the user over a network

i will move this to my business logic in routes side

#TODO
Later i will do email dispatcher so that my routes will
not wait for the email has send successfully or not
"""

from pydantic import EmailStr


from .enums import OTPPurpose
from .generator import OTPGenerator
from .repository import OTPRepository
from ..mail.sender import EmailSender
from ..mail.models import EmailMessageData
from .models import OTPSendResult
from .render import render_login_otp

from app.config import settings


class OTPSendService:
    """
    For Now OTP is just send over Email
    Not over other Sender way, i will think later about those
    """

    def __init__(
        self,
        repository: OTPRepository,
        generator: OTPGenerator,
        sender: EmailSender,
    ) -> None:
        self._repository = repository
        self._generator = generator
        self._sender = sender

    def execute(
        self,
        identifier: EmailStr,
        purpose_str: OTPPurpose,
    ) -> OTPSendResult:
        """
        This will check if otp will send or not by calling the shared/otp related things

        1. Check Cooldown
        2. Generate OTP
        3. clear old cooldown

        """
        # First it will check if this email is block for response for sometime or not
        # if not block it will then try to send the otp to the user
        # TODO

        if self._repository.is_cooldown_active(
            identifier=identifier,
            purpose=purpose_str,
        ):
            return OTPSendResult(
                success=False,
                message="Please Wait Before Request Another OTP in Cooldown...",
            )

        otp = self._generator.generate(
            length=6,
        )

        self._repository.save_otp(
            identifier=identifier,
            purpose=purpose_str,
            otp=otp,
        )

        self._repository.reset_attempt(
            identifier=identifier,
            purpose=purpose_str,
        )

        self._repository.start_cooldown(
            identifier=identifier,
            purpose=purpose_str,
        )

        # later i will make this to the celry to call thia later
        mail_sub = "This Is Your OTP"
        mail_body, mail_html = render_login_otp(
            otp=otp,
            valid_seconds=60,
        )
        # i will call this from the templates.py to genreeat this body
        email_data = EmailMessageData(
            to_email=[
                identifier,
            ],
            subject=mail_sub,
            body_text=mail_body,
            body_html=mail_html,
            reply_to=settings.mail.reply_to_otp,
        )
        self._sender.send_mail(
            email_msg=email_data,
        )
        return OTPSendResult(
            success=True,
            message="OTP Has Started to send to this email id",
        )
