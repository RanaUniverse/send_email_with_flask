"""
app/shared/otp/infrastructer/cooldown.py

This will have the logic only of how to handle the cooldown thigns
"""

from pydantic import EmailStr

from ..interfaces.cooldown import OTPCooldown  # type: ignore
from ..enums import OTPPurpose


class LocalCooldown:
    """
    This is for local testing cooldown
    it will only give some demo data for local development

    For now this u,v,w gmail are in cooldown those should say in cooldown for sometime
    """

    def __init__(self) -> None:
        x = {
            "u@gmail.com",
            "v@gmail.com",
            "w@gmail.com",
            "rana2@rana.com",
        }
        self._cooldown_identifiers: set[str] = x

    def is_active(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
    ) -> bool:
        x = identifier.lower() in self._cooldown_identifiers
        return x

    def start(
        self,
        *,
        identifier: EmailStr,
        purpose: OTPPurpose,
        cooldown_seconds: int,
    ) -> None:
        """
        This will start the cooldown here
        """
        pass
