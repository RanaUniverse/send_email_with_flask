"""
app/shared/otp/factory.py

Here i will out which otp model i will use in my case
"""

from .generator import (
    OTPGenerator,
    LocalTestingOTPGenerator,
    OTPAlphabetGenerator,
    OTPNumberGenerator,
)

from .repository import (
    OTPRepository,
    LocalTestingOTPRepository,
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

    return LocalTestingOTPGenerator()


def get_otp_repository() -> OTPRepository:
    """
    See i will probably use redis in real time
    """
    o = LocalTestingOTPRepository()
    return o


otp_repository_obj = get_otp_repository()
otp_generator_obj = get_otp_generator()
