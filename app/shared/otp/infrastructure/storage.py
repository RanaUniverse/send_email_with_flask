"""
app/shared/otp/infrastructer/cooldown.py

Here i will write the code to store otp thigns in reality how
it maybe redis, db or somethigns
"""

from ..enums import OTPPurpose
from ..interfaces.storage import OTPStorage  # type: ignore


class LocalTestingOTPStorage:
    TEST_OTP = "112233"

    def save_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
        otp: str,
    ) -> None:
        """
        This should to save the otp so that later i can check
        """
        pass

    def get_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> str | None:
        """
        This will try to read the otp from my backend
        whcih was store in some place
        """
        return self.TEST_OTP

    def delete_otp(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        It will try to delete the otp from cache if it need to remove beforehand
        or if this has validate it need to be delete so that noone will complain against this
        """
        pass


class RedisOTPRepository:
    """
    I will use this in relaity to handle the otp by the redis

    Redis will store otp and ttl remove and so on i will follow the
    upper protocol class in this case
    """

    pass
