"""
app/shared/otp/runtime_validation.py

This is where my validation will works of otp realted thigns
"""

from .policy import validate_otp_policies
from .render import validate_otp_email_presentation

from app.config import settings


def validate_all_otp_config() -> None:
    """
    This will call all otp realted validation fun and run here
    """
    validation_mode = settings.app.validation_mode

    if validation_mode == "PRODUCTION":

        validate_otp_policies()
        validate_otp_email_presentation()

    elif validation_mode == "DEVELOPMENT":

        r = "This is in Development Now no validation is running."
        print("---")
        print(r)
        print("---")

    else:
        raise RuntimeError(
            "This is wrong validation_mode",
        )

    # else:
    #     print("Please Choose This Clearly from the .env of validaion mode")
    #     raise RuntimeError(
    #         "You need to choose production or development must",
    #     )
