"""
app/features/identity/models.py

This will have the models or data to keep for this related thigns
"""

from pydantic import BaseModel


from .enums import (
    RegistrationStatus,
    AfterRegistrationNextStep,
    RegistrationOTPStatus,
    RegistrationOTPStatusNextStep,
)


class RegistrationResult(BaseModel):

    status: RegistrationStatus
    next_step: AfterRegistrationNextStep

    @property
    def success(
        self,
    ) -> bool:
        """
        This say true if the registration mail has sent to user
        successfully. maybe mail has dispatched then it will true
        """

        x = self.status == RegistrationStatus.OTP_SENT
        return x


class RegistrationViaOTPResult(BaseModel):
    """
    I will next_step = none when this will be decide by the routes.py
    """

    status: RegistrationOTPStatus
    next_step: RegistrationOTPStatusNextStep | None = None

    def success(
        self,
    ) -> bool:
        """
        This will say true if register has the status of success
        """
        r = self.status == RegistrationOTPStatus.VERIFIED
        return r
