"""
app/shared/security/factory.py

Here i will use the logic to setup the otp of letters or number
i will call this as startup to choose i will use the number or letter.
"""

from .otp_generate import (
    OTPGenerator,
    OTPAlphabetGenerator,
    OTPNumberGenerator,
)


def get_otp_generator() -> OTPGenerator:
    """
    This will choose if i will going to use what
    """
    # TODO
    # later i will get this form the env
    which = True

    if which:
        return OTPNumberGenerator()
    else:
        return OTPAlphabetGenerator()


otp_generator_obj = get_otp_generator()
