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


class LoginStatus(StrEnum):
    OTP_SENT = "otp_sent"
    NO_ACCOUNT = "no_account"
    PROBLEM = "problem"


class LoginOTPStatus(StrEnum):
    VERIFIED = "verified"
    NOT_VERIFIED = "not_verified"


class AfterRegistrationNextStep(StrEnum):
    ENTER_PASSWORD = "enter_password"
    VERIFY_OTP = "verify_otp"
    SHOW_ERROR = "show_error"


class RegistrationOTPStatus(StrEnum):
    """
    Currently i have only implimented the verified and invalid_otp
    """

    VERIFIED = "verified"
    INVALID_OTP = "invalid_otp"
    OTP_NOT_FOUND = "otp_not_found"
    ATTEMPT_LIMIT_EXCEEDED = "attempt_limit_exceeded"
    NOT_VERIFIED = "not_verified"
    # This last one is a generic one i need later not try to use why not


class RegistrationOTPStatusNextStep(StrEnum):
    SET_PASSWORD = "set_password"
    RETRY_OTP = "retry_otp"
    RESTART_REGISTRATION = "restart_registration"
