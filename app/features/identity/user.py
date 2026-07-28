"""
app/features/identity/user.py

Here i will user related settings
"""

from flask_login import UserMixin  # type: ignore


class User(UserMixin):
    def __init__(
        self,
        id_: str | int,
        username: str,
        email: str,
        phone: str,
        balance: float,
    ) -> None:
        self.id_ = str(id_)
        self.username = username
        self.email = email
        self.phone = phone
        self.balance = balance


USER_: dict[str, User] = {
    "1": User(
        1,
        "john",
        "john@gmail.com",
        "8989899889",
        balance=500,
    ),
    "2": User(
        2,
        "roman",
        "roman@reigns.com",
        "5665565665",
        balance=600,
    ),
    "3": User(
        3,
        "brock",
        "brock@lesnar.com",
        "2323233223",
        balance=700,
    ),
}
