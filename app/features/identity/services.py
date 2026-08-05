"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

from app.shared.security.service import OTPService

from app.shared.mail.factory import mail_sender_obj
from app.shared.security.factory import otp_generator_obj

from .domain.email_validation import ValidatedEmail
from .exceptions import InvalidEmailError
from .user import USER_, User


def get_user_from_email(email_id: str) -> User | None:
    for user in USER_.values():
        if user.email == email_id:
            return user

    return None


def check_authentication(
    email: str,
    password: str,
) -> User | None:
    """
    Authenticate a user using an email address and password.

    Returns:
        User: The authenticated user if the credentials are valid.
        None: If authentication fails.
    """
    user_obj = get_user_from_email(
        email_id=email,
    )
    if not user_obj:
        return None

    stored_password = user_obj.password

    if password == stored_password:
        return user_obj


def start_regisration(email: str):
    """
    It need to send otp in background and send response to user
    quickly i will do this later
    Raise:
        InvalidEmailError
    #TODO
    """

    try:
        validated_email_id = ValidatedEmail(email_id=email).value

    except InvalidEmailError:
        raise

    # except ValidationError as e:
    #     error_message = e.errors()[0]["msg"]
    #     raise InvalidEmailError(
    #         f"Invalid Email: {error_message}",
    #     )
    #     # this uppper expose the pydantic error message i need to think #TODO

    sender = mail_sender_obj
    otp_generator = otp_generator_obj

    o = OTPService(
        sender=sender,
        generator=otp_generator,
    )
    o.send_otp(
        email_to=validated_email_id,
    )

    return True
