"""
app/features/identity/presentation/registration_response.py

Here i will decide  what to do based on the registion result of next step
This is related to the routes.py
"""

from flask import (
    redirect,
    url_for,
    flash,
)
from ..application.registration.dto import RegistrationResult
from ..domain.enums import AfterRegistrationNextStep

from app.shared.session.enums import IdentitySessionKey
from app.shared.session.service import set_identity_key as set_identity_key_in_session
from .message import registration_to_flash


def handle_registration_result(
    result: RegistrationResult,
):
    """
    From the routes function i will decide waht to do here based
    on the registration result so that my routes.py will be clean
    """

    information = registration_to_flash(
        result=result,
    )

    flash(
        message=information.message,
        category=information.category,
    )
    # later i will think how i can add phone, email or somethig username
    if result.identity:
        email = result.identity.email
    else:
        email = ""

    match result.next_step:

        case AfterRegistrationNextStep.VERIFY_OTP:

            set_identity_key_in_session(
                key=IdentitySessionKey.REGISTER_PENDING,
                email_value=email,
            )

            return redirect(
                url_for(
                    "auth_bp.verify_otp",
                )
            )

        case AfterRegistrationNextStep.ENTER_PASSWORD:
            set_identity_key_in_session(
                key=IdentitySessionKey.LOGIN_PENDING,
                email_value=email,
            )
            return redirect(
                url_for(
                    "auth_bp.login_with_password",
                )
            )

        case AfterRegistrationNextStep.SHOW_ERROR:

            return redirect(
                url_for(
                    "auth_bp.register",
                )
            )

        case _:
            # i will do some check here later
            flash(
                "Somethign went wrong pls report to admin",
                "warning",
            )
            return redirect(
                url_for(
                    "auth_bp.register",
                )
            )
