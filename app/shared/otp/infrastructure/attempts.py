"""
app/shared/otp/infrastructure/attempts.py

Here i will write the real backend service of how they will have the attempts
"""

from pydantic import EmailStr
from ..interfaces.attempts import OTPAttemptTracker  # type: ignore

from ..enums import OTPPurpose


class LocalOTPAttemptTracker:
    """
    This is for locally development for testing purpose only
    """

    DEFAULT_ATTEMPTS = 1

    def get_attempt_count(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> int:
        return self.DEFAULT_ATTEMPTS

    def increment(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        pass

    def reset(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> None:
        pass
