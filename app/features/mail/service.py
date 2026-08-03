"""
app/features/mail/service.py

Here i will keep the business logic of what to do
or what to validate or not i will call the operations.py
"""

from app.shared.mail.factory import mail_sender

from app.shared.mail.factory import mail_sender
from app.shared.security.service import OTPService

from app.shared.security.factory import otp_generator_obj


def send_otp_to_email(to_email: str):
    """
    Here i will have my business logic to keep cache this
    and then pass to db and so on
    """
    # first i will decide what mail sender to use like my otp or general or what
    sender = mail_sender
    otp_generator = otp_generator_obj

    o = OTPService(
        sender=sender,
        generator=otp_generator,
    )
    o.send_otp(
        email_to=to_email,
    )


def send_email_to_one_user():
    """
    This will just Send the mail to the user or whatsoever
    This is my business logic,
    here it will choose if the mail will go over gmail, local or anything else
    """
    pass
