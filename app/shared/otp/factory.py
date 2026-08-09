"""
app/shared/otp/factory.py

Here i will out which otp model i will use in my case
"""

from .interfaces.attempts import OTPAttemptTracker
from .interfaces.blocklist import BlockList
from .interfaces.cooldown import OTPCooldown
from .interfaces.generator import OTPGenerator
from .interfaces.storage import OTPStorage

from .infrastructure.attempts import LocalOTPAttemptTracker
from .infrastructure.blocklist import LocalInMemoryBlocklist
from .infrastructure.cooldown import LocalCooldown
from .infrastructure.generator import OTPNumberGenerator
from .infrastructure.storage import LocalTestingOTPStorage


def create_otp_attempt_tracker() -> OTPAttemptTracker:
    return LocalOTPAttemptTracker()


def create_otp_cooldown() -> OTPCooldown:
    return LocalCooldown()


def create_otp_generator() -> OTPGenerator:
    return OTPNumberGenerator()


def create_otp_storage() -> OTPStorage:
    return LocalTestingOTPStorage()


# I keep upper fun differntly here so that i can change any logic
# if i want to change any component there


def create_otp_components() -> tuple[
    OTPStorage,
    OTPGenerator,
    OTPCooldown,
    OTPAttemptTracker,
]:
    """
    This is creating all the necessary otp related objects
    i will use those values as dependency injection in my usecase
    """
    attempt_tracker_obj = create_otp_attempt_tracker()
    cooldown_obj = create_otp_cooldown()
    generator_obj = create_otp_generator()
    storage_obj = create_otp_storage()
    return (
        storage_obj,
        generator_obj,
        cooldown_obj,
        attempt_tracker_obj,
    )


def get_blocklist_email() -> BlockList:
    """
    For now locally development it send later i will use real db
    """
    return LocalInMemoryBlocklist()


blocklist_email_obj = get_blocklist_email()
otp_componenet_objects = create_otp_components()
