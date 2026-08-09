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
from .render import render_otp_email
from .policy import get_otp_policy_obj

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
        purpose: OTPPurpose,
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
            purpose=purpose,
        ):
            return OTPSendResult(
                status=OTPSendStatus.COOLDOWN_ACTIVE,
                message="Cooldown is Active Now Wait until cooldown expires",
            )

        otp_policy_obj = get_otp_policy_obj(
            purpose=purpose,
        )

        otp = self._generator.generate(
            length=otp_policy_obj.length,
        )

        self._storage.save_otp(
            identifier=identifier,
            purpose=purpose,
            otp=otp,
            ttl_seconds=otp_policy_obj.validity,
        )

        self._attempt.reset(
            identifier=identifier,
            purpose=purpose,
        )

        self._cooldown.start(
            identifier=identifier,
            purpose=purpose,
            cooldown_seconds=otp_policy_obj.cooldown,
        )

        # TODO
        # later i will make this to the celry to call this later
        mail_data = render_otp_email(
            otp=otp,
            valid_seconds=otp_policy_obj.validity,
            purpose=purpose,
        )
        mail_sub = mail_data.subject
        body_text = mail_data.body_text
        body_html = mail_data.body_html
        # i will call this from the templates.py to genreeat this body
        email_data = EmailMessageData(
            to_email=[
                identifier,
            ],
            subject=mail_sub,
            body_text=body_text,
            body_html=body_html,
            reply_to=settings.mail.reply_to_otp,
        )
        self._sender.send_mail(
            email_msg=email_data,
        )
        return OTPSendResult(
            status=OTPSendStatus.SENT,
            message="OTP Has Successfully Sended to User.",
        )
