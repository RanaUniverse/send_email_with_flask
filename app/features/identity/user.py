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
        password: str,
    ) -> None:
        self.id_ = str(id_)
        self.username = username
        self.email = email
        self.phone = phone
        self.balance = balance
        self.password = password

    def get_id(self):

        return str(self.id_)


USER_: dict[str, User] = {
    "1": User(
        1,
        "john",
        "john@gmail.com",
        "8989899889",
        balance=500,
        password="a",
    ),
    "2": User(
        2,
        "roman",
        "roman@reigns.com",
        "5665565665",
        balance=600,
        password="b",
    ),
    "3": User(
        3,
        "brock",
        "brock@lesnar.com",
        "2323233223",
        balance=700,
        password="c",
    ),
    "4": User(
        4,
        "rana",
        "r@r.com",
        "0000000000",
        balance=1000,
        password="r",
    ),
}
