"""
app/shared/otp/models.py

I will use this for models to reprreset the data
and then i will use this for send or use
"""

from pydantic import BaseModel


from .enums import OTPSendStatus


class OTPSendResult(BaseModel):

    status: OTPSendStatus
    message: str

    @property
    def success(
        self,
    ):
        x = self.status == OTPSendStatus.SENT
        return x
