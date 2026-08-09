"""
app/shared/otp/infrastructure/blocklist.py

i will make real implimentation here of real logics here
"""

from pydantic import EmailStr


from ..interfaces.blocklist import BlockList  # type: ignore


class LocalInMemoryBlocklist:
    """
    This is for local testing only i will use for learning purpose only

    Here i keep some local emails to block them.
    """

    def __init__(self) -> None:
        x = {
            "x@gmail.com",
            "y@gmail.com",
            "z@gmail.com",
            "rana1@rana.com",
        }
        self._blocked_identifiers: set[str] = x

    def is_blocked(
        self,
        identifier: EmailStr,
    ) -> bool:
        """
        only for now check the list of the emails i write here
        """
        x = identifier.lower() in self._blocked_identifiers
        return x
