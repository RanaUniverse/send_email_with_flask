"""
app/features/identity/services/otp.py

Here i will write my otp related services
Like how it will call otp generate, verifications and so on
"""

from app.shared.otp.send import OTPSendService
from app.shared.otp.models import OTPSendResult


from app.shared.otp.factory import (
    otp_generator_obj,
    otp_repository_obj,
)
from app.shared.mail.factory import mail_sender_obj

from app.shared.otp.enums import OTPPurpose


def verify_otp_service(
    email_id: str,
    submitted_otp: str,
) -> bool:
    """
    I will add real checking logic here
    """

    if email_id == "a@gmail.com" and submitted_otp == "123456":
        return True
    return False


def send_login_otp_to_email(
    email_id: str,
    purpose_str: OTPPurpose = OTPPurpose.LOGIN,
) -> OTPSendResult:

    s = OTPSendService(
        repository=otp_repository_obj,
        generator=otp_generator_obj,
        sender=mail_sender_obj,
    )
    mail_send = s.execute(
        identifier=email_id,
        purpose_str=purpose_str,
    )
    return mail_send
