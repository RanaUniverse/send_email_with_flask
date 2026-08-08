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


class OTPSendStatus(StrEnum):
    SENT = "sent"
    COOLDOWN_ACTIVE = "cooldown_active"
    EMAIL_BLOCKED = "email_blocked"
    ATTEMPT_LIMIT_EXCEEDED = "attempt_limit_exceeded"
    EMAIL_SERVER_FAILED = "email_server_failed"
    SEND_FAILED = "send_failed"
