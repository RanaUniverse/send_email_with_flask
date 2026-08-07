"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

from ..domain.email_validation import ValidatedEmail
from ..exceptions import InvalidEmailError
from ..user import USER_, User


from .otp import send_login_otp_to_email


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


def start_regisration(email: str) -> bool:
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

    mail_send = send_login_otp_to_email(
        email_id=validated_email_id,
    )

    if mail_send.success:
        return True
    
    return False
