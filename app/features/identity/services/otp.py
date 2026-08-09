"""
app/features/identity/services/otp.py

Identity specefic OTP operations.

Here i will write my otp related services
Like how it will call otp generate, verifications and so on
"""

from pydantic import EmailStr


from app.shared.otp.send import OTPSendService
from app.shared.otp.models import OTPSendResult

from app.shared.otp.factory import otp_componenet_objects

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


def send_otp_to_email(
    email_id: EmailStr,
    purpose: OTPPurpose,
) -> OTPSendResult:
    """
    Here i need to pass the correct validated email id
    which is not register/login or what so ever in the database and then
    it will just try to send otp to him
    """

    storage_obj, generator_obj, cooldown_obj, attempt_obj = otp_componenet_objects

    s = OTPSendService(
        attempt=attempt_obj,
        cooldown=cooldown_obj,
        generator=generator_obj,
        storage=storage_obj,
        sender=mail_sender_obj,
    )

    mail_send = s.execute(
        identifier=email_id,
        purpose=purpose,
    )

    return mail_send
