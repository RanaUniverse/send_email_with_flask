"""
app/features/identity/presentation/authentication.py

Here i will write my user class for flask_login related thigns
"""

from flask_login import UserMixin  # type: ignore

from ..domain.entities.user import UserDomain


class FlaskLoginUser(UserMixin):
    """
    This present the user class need by flask_login to have here
    """

    def __init__(
        self,
        user: UserDomain,
    ) -> None:
        self._user = user

    def get_id(self):
        """
        I make this as per the docs of the flask_login i need to have a way
        to return the str to uniquely represent a user so that it will
        save in the cookie and later i can get user obj from this

        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        unique_id_represent_the_user = self._user.id_
        return str(unique_id_represent_the_user)
