"""
app/features/identity/models.py

This will have the models or data to keep for this related thigns
"""

from pydantic import BaseModel


from .enums import RegistrationStatus


class RegistrationResult(BaseModel):

    status: RegistrationStatus

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
