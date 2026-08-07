"""
app/shared/otp/repository.py

Here i will defines the otp need what what things
"""

from typing import Protocol


from .enums import OTPPurpose


class OTPRepository(Protocol):
    """
    This will have all the otp related thigns to know by this
    like cooldown, generate or expire how works with its methods.

    This is My Business Logic of When & How to Send or Limit the
    OTP Sending to the user.

    I will use Redis, or DB later which i need to impliment below methods.
    """

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
        ...

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
        ...

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
        ...

    def get_attempts(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> int:
        """
        This will get how many attempt has done for this otp
        """
        ...

    def increment_attempt(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        For wrong attempt it will increment an attmept
        """
        ...

    def reset_attempt(
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

    def is_cooldown_active(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> bool:
        """
        if cooldown active yes or not it will return so that
        i will decide to send another mail or not
        """
        ...

    def start_cooldown(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        This will start a cooldown so that user cannot request for otp
        many time in this time period
        """
        ...


class LocalTestingOTPRepository:
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

    def get_attempts(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> int:
        """
        This will get how many attempt has done for this otp
        """
        return 0

    def increment_attempt(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        For wrong attempt it will increment an attmept
        """
        pass

    def reset_attempt(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        This will reset the attempts to 0
        so that after new otp generate the old attempts not counts
        """
        pass

    def is_cooldown_active(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> bool:
        """
        if cooldown active yes or not it will return so that
        i will decide to send another mail or not
        """
        return False

    def start_cooldown(
        self,
        *,
        identifier: str,
        purpose: OTPPurpose,
    ) -> None:
        """
        This will start a cooldown so that user cannot request for otp
        many time in this time period
        """
        pass


class RedisOTPRepository:
    """
    I will use this in relaity to handle the otp by the redis

    Redis will store otp and ttl remove and so on i will follow the
    upper protocol class in this case
    """

    pass
