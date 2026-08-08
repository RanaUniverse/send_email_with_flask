"""
app/features/identity/enums.py

Here i will keep the needed thigns to easily access this
"""

from enum import StrEnum


class RegistrationStatus(StrEnum):
    OTP_SENT = "otp_sent"

    EMAIL_ALREADY_REGISTERED = "email_already_registered"

    EMAIL_BLOCKED = "email_blocked"
    OTP_COOLDOWN_ACTIVE = "otp_cooldown_active"
    ATTEMPT_LIMIT_EXCEED = "attempt_limit_exceed"

    EMAIL_SERVICE_FAILED = "email_service_failed"
