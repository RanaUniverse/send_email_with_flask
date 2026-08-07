"""
app/shared/otp/models.py

I will use this for models to reprreset the data
and then i will use this for send or use
"""

from pydantic import BaseModel


class OTPSendResult(BaseModel):
    success: bool
    message: str

