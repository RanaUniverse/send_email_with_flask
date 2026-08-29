"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

from pydantic import EmailStr


from ...domain.entities.user import UserDomain
from ...domain.repositories.user_repository import UserRepository


class LoginService:
    """
    Here i will keep login related thigns so easily i can use those
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:

        self._user_repository = user_repository

    def check_authentication(
        self,
        email: EmailStr,
        password: str,
    ) -> UserDomain | None:
        """
        Authenticate a user using an email address and password.

        Returns:
            User: The authenticated user if the credentials are valid.
            None: If authentication fails.
        """
        obj = self._user_repository.get_by_email(
            email=email,
        )
        if not obj:
            return None
        stored_password_hash = obj.hashed_password

        if password == stored_password_hash:
            return obj
