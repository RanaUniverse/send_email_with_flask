"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

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
