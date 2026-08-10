"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

from pydantic import EmailStr


from ..repository.user import UserRepository, User


def check_authentication(
    email: EmailStr,
    password: str,
) -> User | None:
    """
    Authenticate a user using an email address and password.

    Returns:
        User: The authenticated user if the credentials are valid.
        None: If authentication fails.
    """
    u = UserRepository()
    user_obj = u.get_by_email(
        email=email,
    )
    if not user_obj:
        return None

    stored_password = user_obj.password

    if password == stored_password:
        return user_obj
