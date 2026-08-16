"""
app/features/identity/repository/user.py

Here i will keep user related data of how the user checking will be done
"""

from pydantic import EmailStr

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


# This is a demo database to check if user is already register or not
USER_: dict[str, User] = {
    "1": User(
        1,
        "john",
        "a@gmail.com",
        "8989899889",
        balance=500,
        password="a",
    ),
    "2": User(
        2,
        "roman",
        "b@gmail.com",
        "5665565665",
        balance=600,
        password="b",
    ),
    "3": User(
        3,
        "brock",
        "c@gmail.com",
        "2323233223",
        balance=700,
        password="c",
    ),
    # below user 4 should not valid as my business email domain not
    # support the @r.com domain so this should not handle as blocked email
    "4": User(
        4,
        "rana",
        "r@r.com",
        "0000000000",
        balance=1000,
        password="r",
    ),
}


class UserRepository:
    """
    This is have user related information extract methods
    """

    def get_by_email(
        self,
        email: EmailStr,
    ) -> User | None:

        for user in USER_.values():
            if user.email == email:
                return user

        return None

    def exists_by_email(
        self,
        email: EmailStr,
    ) -> bool:

        r = self.get_by_email(email) is not None
        return r

    def add(
        self,
        username: str,
        email: EmailStr,
        phone: str,
        balance: float,
        password: str,
    ) -> User:

        if self.exists_by_email(email):
            raise ValueError(
                "User with this email already exists",
            )

        new_id = str(
            max(
                map(
                    int,
                    USER_.keys(),
                ),
                default=0,
            )
            + 1,
        )

        user = User(
            id_=new_id,
            username=username,
            email=str(email),
            phone=phone,
            balance=balance,
            password=password,
        )

        USER_[new_id] = user
        print("NEW DATA")
        print(USER_, user)
        print("NEW DATA")
        return user
