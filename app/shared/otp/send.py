"""
app/shared/otp/send.py

This is for send otp to the user over a network

i will move this to my business logic in routes side

#TODO
Later i will do email dispatcher so that my routes will
not wait for the email has send successfully or not
"""

from pydantic import EmailStr


from app.config import settings

from .enums import OTPPurpose, OTPSendStatus
from ..mail.sender import EmailSender
from ..mail.models import EmailMessageData
from .models import OTPSendResult
from .render import render_login_otp


from .interfaces.attempts import OTPAttemptTracker
from .interfaces.cooldown import OTPCooldown
from .interfaces.generator import OTPGenerator
from .interfaces.storage import OTPStorage

from .interfaces.blocklist import Blocklist
from .infrastructure.blocklist import localinmemoryblocklist_obj

# TODO i will later use this from the config
# i will do it from reality later when i will impliment this

OTP_BLOCKLIST_ENABLED: bool = True


class OTPSendService:
    """
    For Now OTP is just send over Email
    Not over other Sender way, i will think later about those
    """

    def __init__(
        self,
        attempt: OTPAttemptTracker,
        cooldown: OTPCooldown,
        generator: OTPGenerator,
        storage: OTPStorage,
        sender: EmailSender,
    ) -> None:
        self._attempt = attempt
        self._cooldown = cooldown
        self._generator = generator
        self._storage = storage
        self._sender = sender

        # For now i make this here later i will make this with di
        # as still this is developing i am making this here
        self._blocklist: Blocklist = localinmemoryblocklist_obj

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

        if OTP_BLOCKLIST_ENABLED:
            if self._blocklist.is_blocked(
                identifier=identifier,
            ):
                return OTPSendResult(
                    status=OTPSendStatus.EMAIL_BLOCKED,
                    message="This Email is Blocked ",
                )

        if self._cooldown.is_active(
            identifier=identifier,
            purpose=purpose_str,
        ):
            return OTPSendResult(
                status=OTPSendStatus.COOLDOWN_ACTIVE,
                message="Cooldown is Active",
            )

        otp = self._generator.generate(
            length=6,
        )

        self._storage.save_otp(
            identifier=identifier,
            purpose=purpose_str,
            otp=otp,
        )

        self._attempt.reset(
            identifier=identifier,
            purpose=purpose_str,
        )
        self._cooldown.start(
            identifier=identifier,
            purpose=purpose_str,
        )

        # TODO
        # later i will make this to the celry to call this later
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
            status=OTPSendStatus.SENT,
            message="OTP Has Successfully Sended to User.",
        )
