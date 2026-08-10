"""
app/features/identity/operations.py

Here i will keep write some db operations
"""

from .repository.user import (
    User,
    USER_,
)


def get_user_by_id(user_id: str) -> User | None:
    """
    it will get the user_id of string and return the full user_obj
    as i will call this in flask's user_loader fun
    """
    obj = USER_.get(str(user_id), None)
    return obj
