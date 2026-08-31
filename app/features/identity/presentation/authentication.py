"""
app/features/identity/presentation/authentication.py

Here i will write my user class for flask_login related thigns
"""

from typing import cast


from flask_di import (
    Depends,
    current_app,
)

from flask_login import (  # type: ignore
    UserMixin,
)

from ..domain.entities.user import UserDomain

from ..domain.repositories.user_repository import UserRepository

from ..dependencies import user_repository_provider

from app.shared.extensions import login_manager


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

    @property
    def domain_user(self) -> UserDomain:
        return self._user


# # TODO
# # i need to make sure to resolve the di fun of user_repository below
# @login_manager.user_loader
# def load_user(
#     user_id: str,
#     user_repository: UserRepositoryDep,
# ) -> FlaskLoginUser | None:
#     """
#     https://flask-login.readthedocs.io/en/latest/#how-it-works
#     As per the docs it should return the obj or the None.

#     This will read the user_id from the cookie and convert into the user obj
#     from the user_obj i will get differnt data to use.
#     """
#     obj_entity = user_repository.get_by_id(
#         user_id=user_id,
#     )

#     if obj_entity is None:
#         return None

#     return FlaskLoginUser(obj_entity)


@login_manager.user_loader  # type: ignore
def load_user(
    user_id: str,
) -> FlaskLoginUser | None:
    """
    https://flask-login.readthedocs.io/en/latest/#how-it-works
    As per the docs it should return the obj or the None.

    This will read the user_id from the cookie and convert into the user obj
    from the user_obj i will get differnt data to use.
    """

    # later i will upgrde this library and solve this #TODO
    user_repository_old = current_app._resolve_dependency(  # type: ignore
        Depends(
            user_repository_provider,
        )
    )
    user_repository = cast(UserRepository, user_repository_old)

    obj_domain = user_repository.get_by_id(
        user_id,
    )

    if obj_domain is None:
        return None

    obj = FlaskLoginUser(
        obj_domain,
    )
    return obj

    # This below is for testing to check
    # return FlaskLoginUser(
    #     UserDomain(
    #         id_="abc",
    #         email="a@b.com",
    #         hashed_password="s",
    #     )
    # )
