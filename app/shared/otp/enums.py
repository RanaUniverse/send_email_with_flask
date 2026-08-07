"""
app/shared/otp/enums.py

Here i will keep write this other will import this
this module will not import anything
"""

from enum import StrEnum


class OTPPurpose(StrEnum):
    REGISTER = "register"
    LOGIN = "login"
    FORGET_PASSWORD = "forget_password"
    ORDER_CONFIRMATION = "order_confirmation"
