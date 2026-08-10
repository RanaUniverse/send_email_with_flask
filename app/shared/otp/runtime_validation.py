"""
app/shared/otp/runtime_validation.py

This is where my validation will works of otp realted thigns
"""

from .policy import validate_otp_policies
from .render import validate_otp_email_presentation


def validate_all_otp_config() -> None:
    """
    This will call all otp realted validation fun and run here
    """

    validate_otp_policies()
    validate_otp_email_presentation()
