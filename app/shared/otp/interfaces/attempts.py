"""
app/shared/otp/interfaces/attempts.py

This will keep tracks of the attemps the user has already done
"""

from typing import Protocol


from pydantic import EmailStr


from ..enums import OTPPurpose


class OTPAttemptTracker(Protocol):
    """
    1. get_attempt_count()
    2. increment()
    3. reset()

    It will have all the attempts related records and so on
    """

    def get_attempt_count(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> int:
        """
        This will shows how many attempts has been alreay done
        """
        ...

    def increment(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        For wrong attempt it will increment an attmept
        """
        ...

    def reset(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        This will reset the attempts to 0
        so that after new otp generate the old attempts not counts
        """
        ...
