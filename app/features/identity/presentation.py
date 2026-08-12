"""
app/features/identity/presentation.py

This say how the UI will displayed.

This is for taking the data from the service and make this
to usable ui text to shows to user via routes.py
"""

from wtforms.validators import Length


from pydantic import BaseModel


from .enums import RegistrationStatus
from .forms import OTPForm
from .models import RegistrationResult

from app.shared.frontend.enums import FlashCategory
from app.shared.otp.enums import OTPPurpose
from app.shared.otp.policy import get_otp_policy_obj


class PresentationMessageFlask(BaseModel):
    message: str
    category: FlashCategory = FlashCategory.INFO


def registration_to_flash(
    result: RegistrationResult,
) -> PresentationMessageFlask:
    """
    This will take the result of the service.py and make this
    shows the message to the user to shows in the ui
    """

    messages = {
        RegistrationStatus.OTP_SENT: PresentationMessageFlask(
            message="🎉 OTP sent successfully! Please check your email "
            "and enter the OTP to continue.",
            category=FlashCategory.SUCCESS,
        ),
        RegistrationStatus.EMAIL_ALREADY_REGISTERED: PresentationMessageFlask(
            message="📧 This email is already registered. Please log in "
            "with your password instead.",
            category=FlashCategory.PRIMARY,
        ),
        RegistrationStatus.EMAIL_BLOCKED: PresentationMessageFlask(
            message="🚫 This email address is currently blocked. Please "
            "contact support if you believe this is a mistake.",
            category=FlashCategory.DANGER,
        ),
        RegistrationStatus.OTP_COOLDOWN_ACTIVE: PresentationMessageFlask(
            message="⏳ An OTP was recently sent to your email. Please wait "
            "a little before requesting another one.",
            category=FlashCategory.WARNING,
        ),
        RegistrationStatus.ATTEMPT_LIMIT_EXCEED: PresentationMessageFlask(
            message="⚠️ You've reached the maximum number of registration "
            "attempts. Please try again later.",
            category=FlashCategory.WARNING,
        ),
        RegistrationStatus.EMAIL_SERVICE_FAILED: PresentationMessageFlask(
            message="📨 We couldn't send the OTP email right now. Please try "
            "again in a few moments.",
            category=FlashCategory.DANGER,
        ),
    }

    x = messages.get(
        result.status,
        PresentationMessageFlask(
            message="❌ Something went wrong while processing your registration. Please try again. Pls Report The Admin",
            category=FlashCategory.DANGER,
        ),
    )

    return x

    # i keep this as a safety net so that later i can use this easily
    raise RuntimeError(
        f"Unhandled registration status: {result.status}",
    )


def configure_registration_otp_form(
    form: OTPForm,
) -> OTPForm:

    policy = get_otp_policy_obj(
        purpose=OTPPurpose.REGISTER,
    )
    form.otp.label.text = f"Enter {policy.length} Digit OTP"
    form.otp.validators.append(  # type: ignore
        Length(
            min=policy.length,
            max=policy.length,
        )
    )
    return form
